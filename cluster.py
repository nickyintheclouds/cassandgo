#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,datetime,time,boto,boto.ec2
from aws import conf_HVM,keysDir,checkInstance,logError,createInstance,getInstancesRegionZone,terminateInstance
import server,latency

default_node_type = 'm3.large'
default_nb_seeds_per_dc = 1

def destroyCluster(infosDC,cluster_name):
	# we parse per DC all instances tagged with that cluster_name
	print
	print "Removing Cluster instances..."
	print "-"*80
	for infoDC in infosDC:
		print infoDC['datacenter']
		print '-'*80
		instances = getInstancesRegionZone(infoDC['region'],str(infoDC['zone']))
		for instance in instances:
			if ('Cluster' in instance.tags.keys()):
				if ((instance.tags['Cluster'] == cluster_name) and (instance.state != 'terminated')):
					print "Terminate Node "+instance.tags['Name']+' in '+infoDC['region']+'-'+str(infoDC['zone'])
					terminateInstance(infoDC['region'],str(infoDC['zone']),instance.id)

def createCluster(infosDC,cluster_name):
	"""
	Create a Multi-DC Cassandra cluster
	"""
	clusters = []
	total_nodes = 0
	print
	print "Cluster creation..."
	print "-"*80
	for infoDC in infosDC:
		total_nodes += infoDC['nodes']

		# Params by default
		node_type = infoDC['node_type'] if 'node_type' in infoDC else default_node_type
		nb_seeds_per_dc = infoDC['nb_seeds_per_dc'] if 'nb_seeds_per_dc' in infoDC else default_nb_seeds_per_dc
		opscenter = infoDC['opscenter'] if 'opscenter' in infoDC else True

		if opscenter:
			print "Cluster",cluster_name," in ",(infoDC['region']+'-'+str(infoDC['zone']))," :",infoDC['nodes']," nodes [",node_type,"] ",nb_seeds_per_dc," seed(s) opsCenter:",opscenter
		else:
			print "Cluster",cluster_name," in ",(infoDC['region']+'-'+str(infoDC['zone']))," :",infoDC['nodes']," nodes [",node_type,"] ",nb_seeds_per_dc," seed(s) "
		res = createClusterDC(infoDC['datacenter'],infoDC['region'],str(infoDC['zone']),infoDC['nodes'],node_type,nb_seeds_per_dc,cluster_name,opscenter)
		if res:
			clusters.append(res)
		else:
			logError("Error during cluster creation ! :"+str(infoDC))
			return None

	# Waiting for initalized and running nodes
	print 
	print "Waiting for nodes..."
	print "-"*80
	time.sleep(10);
	bUP = False
	while not bUP:
		for cluster in clusters:
			for instance in cluster['instances']:
				# Instance running ?
				if instance['instance'].state == 'running':
					if 'Ready' not in instance['instance'].tags.keys():
						if checkInstance(instance['instance']):
							# Node is Ready
							total_nodes -= 1
							instance['instance'].add_tag('Ready', 1)
							instance['running'] = datetime.datetime.now()
							dt = instance['running'] - instance['creation']
							duration = (dt.days * 24 * 60 * 60 + dt.seconds)
							instance['creation_duration'] = duration
							print cluster['datacenter'] + ' : Node ' + instance['index'] + ' in ' + instance['AZ'] + ' -> OK [' + str(duration) + 's] IP:' + instance['instance'].ip_address + '/' + instance['instance'].private_ip_address
				else:
					instance['instance'].update()
		time.sleep(2)
		if total_nodes == 0:
			break
	print 
	delay = 180
	print "Waiting for Cassandra warmup on all nodes (",delay,"s)..."
	print "-"*80
	time.sleep(delay)

	print 
	print "Stopping Cassandra, opsCenter and Datastax agent on all nodes..."
	print "-"*80
	for cluster in clusters:
		for instance in cluster['instances']:
			print cluster['datacenter'] + ' : Node ' + instance['index'] + ' in ' + instance['AZ']
			key_path = os.path.join(os.path.expanduser(keysDir),'Key-'+instance['region']+'-'+instance['zone']+'.pem')
			cmd = boto.manage.cmdshell.sshclient_from_instance(instance['instance'],key_path,user_name='ubuntu')
			bRunning = False
			while not bRunning:
				res = server.statusCassandra(cmd)
				if 'is running' in res[1]:
					bRunning = True
				else:
					time.sleep(5)
			server.stopCassandra(cmd)
			server.stopDataStaxAgent(cmd)
			if ((cluster['opscenter'] == True) and (instance['index'] == '1')):
				server.stopOpsCenter(cmd)

	print 
	print "Cleaning cassandra data files on all nodes..."
	print "-"*80
	time.sleep(30)
	for cluster in clusters:
		for instance in cluster['instances']:
			print cluster['datacenter'] + ' : Node ' + instance['index'] + ' in ' + instance['AZ']
			key_path = os.path.join(os.path.expanduser(keysDir),'Key-'+instance['region']+'-'+instance['zone']+'.pem')
			cmd = boto.manage.cmdshell.sshclient_from_instance(instance['instance'],key_path,user_name='ubuntu')
			server.cleanCassandra(cmd)

	# Multiple Region ?
	snitch = "Ec2Snitch"
	regions = set([])
        for cluster in clusters:
        	for instance in cluster['instances']:
			regions.add(instance['region']+instance['zone'])
	if (len(regions) > 1):
		# Multiple
		snitch = "Ec2MultiRegionSnitch"

	# Enumerate seeds by DC
	bOpsCenterExists = False
	for cluster in clusters:
		cluster['opsCenterServer'] = None
		cluster['InternalSeeds'] = list()
		cluster['ExternalSeeds'] = list()
		for instance in cluster['instances']:
			print cluster['datacenter'] + ' : Node ' + instance['index'] + ' in ' + instance['AZ']
			if ((cluster['opscenter'] == True) and (instance['index'] == '1')):
				cluster['opsCenterServer'] = {'publicIP':instance['instance'].ip_address,'privateIP':instance['instance'].private_ip_address,'instance':instance['instance'],'regionZone':instance['region']+'-'+instance['zone']}
				bOpsCenterExists = True
			if (len(cluster['InternalSeeds']) < cluster['nb_seeds_per_dc']):
				cluster['InternalSeeds'].append(instance['instance'].private_ip_address)
				cluster['ExternalSeeds'].append(instance['instance'].ip_address)

	# seeds merge
	for i in range(len(clusters)):
		clusters[i]['Seeds'] = list(clusters[i]['InternalSeeds'])
		for j in range(len(clusters)):
			if j != i:
				clusters[i]['Seeds'] += clusters[j]['ExternalSeeds'] 
	print 
	print "Updating cassandra.yaml and DataStax agent conf on all nodes..."
	print "-"*80
	for cluster in clusters:
		for instance in cluster['instances']:
			print cluster['datacenter'] + ' : Node ' + instance['index'] + ' in ' + instance['AZ']
			key_path = os.path.join(os.path.expanduser(keysDir),'Key-'+instance['region']+'-'+instance['zone']+'.pem')
			cmd = boto.manage.cmdshell.sshclient_from_instance(instance['instance'],key_path,user_name='ubuntu')
			server.updateCassandraYaml(cmd,cluster['Seeds'],instance['instance'].ip_address,snitch)
			# Config DataStax agent
			if cluster['opsCenterServer']:
				# There is an OpsCenter Server on this DC, so we use the private ip address for agent stomp_interface
				server.updateDataStaxAgent(cmd,cluster['opsCenterServer']['privateIP'])
			else:
				# no OpsCenter server on this DC, we search an available server in other DCs
				# Priority on opsCenter server on the same Region and Zone
				bStomp = False
				for cluster2 in clusters:
					if cluster2 != cluster:
						if cluster2['opsCenterServer']:
							if (cluster2['opsCenterServer']['regionZone'] == (instance['region']+'-'+instance['zone'])):
								# same Region and Zone, we could use the private ip address for agent stomp_interface
								server.updateDataStaxAgent(cmd,cluster2['opsCenterServer']['privateIP'])
								bStomp = True
								break
				# If not found, we searcg for an OpsCenter server in another Region Zone
				if not bStomp:
					for cluster2 in clusters:
						if cluster2 != cluster:
							if cluster2['opsCenterServer']:
								# we use the public ip address for agent stomp_interface
								server.updateDataStaxAgent(cmd,cluster2['opsCenterServer']['publicIP'])
								bStomp = True
								break

	print 
	print "Starting Cassandra Seeds nodes..."
	print "-"*80
	for cluster in clusters:
		nb_seeds = 0
		for instance in cluster['instances']:
			if ((nb_seeds < cluster['nb_seeds_per_dc']) and (int(instance['index']) <= cluster['nb_seeds_per_dc'])):
				nb_seeds += 1
				print cluster['datacenter'] + ' : Node ' + instance['index'] + ' in ' + instance['AZ']
				key_path = os.path.join(os.path.expanduser(keysDir),'Key-'+instance['region']+'-'+instance['zone']+'.pem')
				cmd = boto.manage.cmdshell.sshclient_from_instance(instance['instance'],key_path,user_name='ubuntu')
				server.startCassandra(cmd)
				time.sleep(30)

	print 
	print "Starting Cassandra on all other nodes..."
	print "-"*80
	time.sleep(10)
	for cluster in clusters:
		nb_seeds = 0
		for instance in cluster['instances']:
			if ((nb_seeds < cluster['nb_seeds_per_dc']) and (int(instance['index']) <= cluster['nb_seeds_per_dc'])):
				nb_seeds += 1
				server.startDataStaxAgent(cmd)
				time.sleep(5)
			else:
				print cluster['datacenter'] + ' : Node ' + instance['index'] + ' in ' + instance['AZ']
				key_path = os.path.join(os.path.expanduser(keysDir),'Key-'+instance['region']+'-'+instance['zone']+'.pem')
				cmd = boto.manage.cmdshell.sshclient_from_instance(instance['instance'],key_path,user_name='ubuntu')
				server.startCassandra(cmd)
				server.startDataStaxAgent(cmd)
				time.sleep(5)

	if bOpsCenterExists:
		print 
		print "Starting OpsCenter..."
		print "-"*80
		time.sleep(10)
		for cluster in clusters:
			if cluster['opsCenterServer']:
				key_path = os.path.join(os.path.expanduser(keysDir),'Key-'+cluster['opsCenterServer']['regionZone']+'.pem')
				cmd = boto.manage.cmdshell.sshclient_from_instance(cluster['opsCenterServer']['instance'],key_path,user_name='ubuntu')
				server.startOpsCenter(cmd)
				print cluster['datacenter'] + ' : Node 1 in ' + cluster['opsCenterServer']['regionZone']

		print 
		print "Starting DataStax Agents..."
		print "-"*80
		time.sleep(10)
		for cluster in clusters:
			for instance in cluster['instances']:
				print cluster['datacenter'] + ' : Node ' + instance['index'] + ' in ' + instance['AZ']
				key_path = os.path.join(os.path.expanduser(keysDir),'Key-'+instance['region']+'-'+instance['zone']+'.pem')
				cmd = boto.manage.cmdshell.sshclient_from_instance(instance['instance'],key_path,user_name='ubuntu')
				server.startDataStaxAgent(cmd)
				time.sleep(5)

	print 
	print "Cassandra cluster finalization..."
	print "-"*80
	time.sleep(30)

	print 
	print "Intra-Cluster latencies..."
	print "-"*80
	for cluster in clusters:
		latency.getLatenciesRegion(cluster)

	print 
	print "Inter-Cluster latencies..."
	print "-"*80
	for i in range(len(clusters)):
		if (i == 0):
			dcs = []
			for j in range(len(clusters)):
				dcs.append(clusters[j]['datacenter'])
			latency.printLatency(clusters,dcs)
			print
		j = i+2
		while (j < len(clusters)):
			dcs = [clusters[i]['datacenter'],clusters[j]['datacenter']]
			latency.printLatency(clusters,dcs)
			print
			j += 1

	print 
	print "How to connect to "+cluster_name+"'s nodes..."
	print "-"*80
	for cluster in clusters:
		print '['+cluster['datacenter']+'] '+cluster['region']+'-'+cluster['zone']
		print "-"*80
		for instance in cluster['instances']:
			print 'Node '+instance['index']+' : ssh -i '+keysDir+'/Key-'+cluster['region']+'-'+cluster['zone']+'.pem ubuntu@'+instance['instance'].ip_address	
		print

	if bOpsCenterExists:
		# Restart OpsCenterServer
		print
		print "Connect to OpsCenter"
		print "-"*80
		for cluster in clusters:
			if cluster['opsCenterServer']:
				key_path = os.path.join(os.path.expanduser(keysDir),'Key-'+cluster['opsCenterServer']['regionZone']+'.pem')
				cmd = boto.manage.cmdshell.sshclient_from_instance(cluster['opsCenterServer']['instance'],key_path,user_name='ubuntu')
				server.restartOpsCenter(cmd)
				print 'http://'+cluster['opsCenterServer']['publicIP']+':8888'

	print
	print "Cluster status..."
	print "-"*80
	instance = clusters[0]['instances'][0]
	key_path = os.path.join(os.path.expanduser(keysDir),'Key-'+instance['region']+'-'+instance['zone']+'.pem')
	cmd = boto.manage.cmdshell.sshclient_from_instance(instance['instance'],key_path,user_name='ubuntu')
	print server.clusterStatus(cmd)
	print

	return clusters
		
def createClusterDC(datacenter,region,zone,nodes,node_type,nb_seeds_per_dc,cluster_name,opscenter):
	cluster = {'cluster':cluster_name,'datacenter':datacenter,'region':region,'zone':zone,'nodes':nodes,'node_type':node_type,'nb_seeds_per_dc':nb_seeds_per_dc,'instances':[],'opscenter':opscenter}
	try:
		# Connection
		ec2 = boto.ec2.connect_to_region(region+'-'+zone)

		# AZ disponibles
		AZlist = ec2.get_all_zones()
		AZ = []
		for AZitem in AZlist:
			if AZitem.state == 'available':
				AZ.append(AZitem.name)
		if (len(AZ) == 0):
			# No available zone
			print "No available AZ !"
			return None

		# On récupère les infos pour l'AMI, key, SG
		info = filter(lambda x: ((x['region'] == region) and (x['zone'] == zone)), conf_HVM)[0]

		# Onlyne one AZ available ?
		if (len(AZ) == 1):
			# we create all instances in the same AZ
			createInstance(ec2,info['ami'],nodes,AZ[0],node_type,info['key'],info['sg'],'--clustername '+cluster_name+' --totalnodes '+str(nodes)+' --version community')
		else:
			# we cycle Availability Zones
			iAZ = 0
			for i in range(nodes):
				if ((i == 0) and (opscenter == True)):
					# On installe OpsCenter sur ce premier noeud Master
					instance = createInstance(ec2,info['ami'],1,AZ[iAZ],node_type,info['key'],info['sg'],'--clustername '+cluster_name+' --totalnodes 1 --version community')
				else:
					# Node without opscenter
					instance = createInstance(ec2,info['ami'],1,AZ[iAZ],node_type,info['key'],info['sg'],'--clustername '+cluster_name+' --opscenter no --totalnodes 1 --version community')
				node_name = "["+datacenter+"] "
				if i == 0:
					node_name += ' M '
				else:
					node_name += ' '+str(i+1)+' '
				node_name += cluster_name
				time.sleep(5)
				instance.add_tag('Name', node_name)
				instance.add_tag('Cluster', cluster_name) 
				cluster['instances'].append({'instance':instance,'index':str(i+1),'creation':datetime.datetime.now(),'region':region,'zone':zone,'datacenter':datacenter,'AZ':AZ[iAZ]})
				iAZ += 1
				if (iAZ == len(AZ)):	iAZ = 0

		return cluster
			
	except Exception as e:
		logError(e)
		return None

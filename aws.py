#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys,logging,socket,collections,boto,boto.ec2

# Init
conf_HVM = [        # DataStax AMI in all regions
{'region':'us-east','zone':'1','ami':'ami-ada2b6c4','sg':'SG-Cassandra-us-east-1','key':'Key-us-east-1'},
{'region':'us-west','zone':'1','ami':'ami-3cf7c979','sg':'SG-Cassandra-us-west-1','key':'Key-us-west-1'},
{'region':'us-west','zone':'2','ami':'ami-1cff962c','sg':'SG-Cassandra-us-west-2','key':'Key-us-west-2'},
{'region':'eu-west','zone':'1','ami':'ami-7f33cd08','sg':'SG-Cassandra-eu-west-1','key':'Key-eu-west-1'},
{'region':'ap-southeast','zone':'1','ami':'ami-b47828e6','sg':'SG-Cassandra-ap-southeast-1','key':'Key-ap-southeast-1'},
{'region':'ap-southeast','zone':'2','ami':'ami-55d54d6f','sg':'SG-Cassandra-ap-southeast-2','key':'Key-ap-southeast-2'},
{'region':'ap-northeast','zone':'1','ami':'ami-714a3770','sg':'SG-Cassandra-ap-northeast-1','key':'Key-ap-northeast-1'},
{'region':'sa-east','zone':'1','ami':'ami-1dda7800','sg':'SG-Cassandra-sa-east-1','key':'Key-sa-east-1'}
]

keysDir = 'keys'    # Directory for saving key pairs


SecurityGroupRule = collections.namedtuple("SecurityGroupRule", ["ip_protocol", "from_port", "to_port", "cidr_ip", "src_group_name"])

CASSANDRA_RULES = [
    SecurityGroupRule("tcp", "22", "22", "0.0.0.0/0", None),
    SecurityGroupRule("tcp", "8888", "8888", "0.0.0.0/0", None),
    SecurityGroupRule("tcp", "9042", "9042", "0.0.0.0/0", None),
    SecurityGroupRule("tcp", "9160", "9160", "0.0.0.0/0", None),
    SecurityGroupRule("tcp", "7000", "7001", "0.0.0.0/0", None),
    SecurityGroupRule("tcp", "1024", "65535", "0.0.0.0/0", "SG"),
    SecurityGroupRule("tcp", "7199", "7199", "0.0.0.0/0", "SG"),
    SecurityGroupRule("tcp", "61621", "61621", "0.0.0.0/0", "SG"),
    SecurityGroupRule("tcp", "61620", "61620", "0.0.0.0/0", None),
    SecurityGroupRule("icmp", "-1", "-1", "0.0.0.0/0", None),
]

def logError(msg):
	logging.error(msg)
	print "ERROR :",msg
	print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)

def checkInstance(instance):
	"""
	Check if an instance is up and running and responding to ssh request
	"""
	res = False
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
	 	s.connect((instance.ip_address, 22))
		res = True
	except socket.error as e:
	    pass
	s.close()
	return res

def terminateInstance(region,zone,instance_id):
	"""
	Terminate an ec2 instance
	"""
	try:
		ec2 = boto.ec2.connect_to_region(region+'-'+zone)
		ec2.terminate_instances(instance_ids=[instance_id])
		return True
	except Exception as e:
		logError(e)
		return False

def createInstance(ec2,ami,nb_nodes,placement,instance_type,key,sg,user_data=None):
    """
    Create a new EC2 instance with specific parameters
    SecurityGroup (sg) and KeyPair (key) have to be previously created (see cassandgo initSG and cassandgo initKP)
    """

    reservation = ec2.run_instances(ami,min_count=nb_nodes,max_count=nb_nodes,placement = placement,key_name=key,security_groups=[sg],instance_type=instance_type,user_data=user_data)
    instance = reservation.instances[0]
    return instance

def createSG(ec2,name,rules):
	"""
	Create a new SecurityGroup
	"""
	# check if the security group exists
	group = None
	sgGroups = [sg for sg in ec2.get_all_security_groups() if sg.name == name]
	if sgGroups:
		group = sgGroups[0]
		ec2.delete_security_group(name=name, group_id=group)	
	print "Creating %s Security Group" % name
	group = ec2.create_security_group(name, 'group for %s' % name)
	if group:
		# Set the inbound rules
		for rule in rules:
			if rule.src_group_name:
				group.authorize(ip_protocol=rule.ip_protocol,from_port=rule.from_port,to_port=rule.to_port,cidr_ip=rule.cidr_ip,src_group=group)
			else:
				group.authorize(ip_protocol=rule.ip_protocol,from_port=rule.from_port,to_port=rule.to_port,cidr_ip=rule.cidr_ip,src_group=None)
		return True
	else:
		logError('Error during '+name+' Security Group update')
		return False


def getInstancesRegionZone(region,zone):
	try:
		ec2 = boto.ec2.connect_to_region(region+'-'+zone)
		instances = []
		all_inst = ec2.get_all_instances()
		for res in all_inst: 
			for instance in res.instances: 
				instances.append(instance)
		return instances
	except Exception as e:
		logError(e)
		return None

def listInstancesRegionZone(region,zone):
	"""
	List all instances for a specific region and zone
	"""
	print "-"*80
	print "# Region :",region," Zone", zone	
	print "-"*80
	instances = getInstancesRegionZone(region,zone)
	if instances:
		for instance in instances:
			print "[",instance.ami_launch_index,"]",instance.ip_address," (",instance.private_ip_address,") ",instance.instance_type," key=",instance.key_name

def createAllSG():
	"""
	Create all Cassandra security groups in all regions
	"""
	for info in conf_HVM:
		ec2 = boto.ec2.connect_to_region(info['region']+'-'+info['zone'])
		createSG(ec2,'SG-Cassandra-'+info['region']+'-'+info['zone'],CASSANDRA_RULES)

def createAllKP():
	"""
	Create all key pairs in all regions
	"""
	if not os.path.exists(keysDir):
		os.makedirs(keysDir)
	for info in conf_HVM:
		keyName = 'Key-'+info['region']+'-'+info['zone']
		try:
			os.remove(keysDir+'/'+keyName+'.pem')
		except OSError:
			pass
		print "Key creation :",keyName
		ec2 = boto.ec2.connect_to_region(info['region']+'-'+info['zone'])
		# check if the key pair exists
		kps = [kp for kp in ec2.get_all_key_pairs() if kp.name == keyName]
		if kps:
			ec2.delete_key_pair(keyName)	
		key = ec2.create_key_pair(keyName)
		key.save(keysDir)

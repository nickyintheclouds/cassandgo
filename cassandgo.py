#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys,yaml,logging
import aws,server,latency,cluster
import pprint

logging.basicConfig(filename='cassandgo.log',level=logging.DEBUG,format='%(asctime)s %(message)s')

"""
####################################################
cassandgo : Cassandra AWS Multi-DC Cluster Generator
####################################################

usage:

cassango initSG

-> create Security Groups in all regions : name SG-Cassandra-[region]-[zone]

cassandgo initKP

-> create Key pairs in all regions : name = Key-[region]-[zone]

cassandra create

--> create the multi-DC cassandra cluster defined in external cassandgo.yaml file

cassandra destroy

--> destroy the cluster defined in cassandgo.yaml
"""

argc = len(sys.argv)
if argc == 1:
	print """
####################################################
cassandgo : Cassandra AWS Multi-DC Cluster Generator
####################################################

usage:

cassandgo initSG (create SecurityGroups in all AWS regions)
cassandgo initKP (create Key pairs in all AWS regions, stored in keys subdirectory)
cassandgo create <clusterName> (create Cassandra Multi-DC cluster based on cassandgo.yaml configuration file)
cassandgo destroy <clusterName> (destroy a specific Cassandra cluster)
"""
	sys.exit(1)
elif argc == 2:
	if sys.argv[1] == 'initSG':
		# Security Group creation
		aws.createAllSG()
	elif sys.argv[1] == 'initKP':
		# Key pairs creation
		aws.createAllKP()
	else:
		print "Unknown operation !"
	sys.exit(1)
elif argc == 3:
	if sys.argv[1] == 'create':
		# Cluster creation
		cluster_name = sys.argv[2]
		stream = open('cassandgo.yaml','r')
		conf = yaml.load(stream)
		if cluster_name in conf:
			cluster.createCluster(conf[cluster_name],cluster_name)
		else:
			print cluster_name+' is not defined !'
	elif sys.argv[1] == 'destroy':
		# Cluster creation
		cluster_name = sys.argv[2]
		stream = open('cassandgo.yaml','r')
		conf = yaml.load(stream)
		if cluster_name in conf:
			cluster.destroyCluster(conf[cluster_name],cluster_name)
		else:
			print cluster_name+' is not defined !'

#for info in conf_HVM:
#	listInstancesRegionZone(info['region'],info['zone'])
#	ec2 = boto.ec2.connect_to_region(info['region']+'-'+info['zone'])

#print createCluster('eu-west','1',3,node_type,'BlaBlaC')

#cluster_name = 'BBCCluster'
#infosDC = [{'datacenter':'DC1','region':'eu-west','zone':'1','nb_nodes':3,'instance_type':node_type,'opsCenter':True},{'datacenter':'DC2','region':'us-east','zone':'1','nb_nodes':3,'instance_type':node_type,'opsCenter':False}]
#infosDC = [{'datacenter':'DC1','region':'eu-west','zone':'1','nb_nodes':6,'instance_type':node_type,'opsCenter':True},{'datacenter':'DC2','region':'us-east','zone':'1','nb_nodes':6,'instance_type':node_type,'opsCenter':False},{'datacenter':'DC3','region':'sa-east','zone':'1','nb_nodes':6,'instance_type':node_type,'opsCenter':False}]
#infosDC = [{'datacenter':'DC1','region':'eu-west','zone':'1','nb_nodes':6,'instance_type':node_type,'opsCenter':True}]
#infosDC = [{'datacenter':'DC1','region':'eu-west','zone':'1','nb_nodes':2,'instance_type':node_type,'opsCenter':True},{'datacenter':'DC2','region':'us-east','zone':'1','nb_nodes':2,'instance_type':node_type,'opsCenter':False}]
#infosDC = [{'datacenter':'DC1','region':'eu-west','zone':'1','nb_nodes':6,'instance_type':node_type,'opsCenter':True},{'datacenter':'DC2','region':'us-east','zone':'1','nb_nodes':6,'instance_type':node_type,'opsCenter':False},{'datacenter':'DC3','region':'us-west','zone':'1','nb_nodes':6,'instance_type':node_type,'opsCenter':False}]
#print createCluster(infosDC,cluster_name)

#ec2 = boto.ec2.connect_to_region('eu-west-1')
#reservations = ec2.get_all_instances(filters={'instance-id' : 'i-8ea2c5ce'})
#instance = reservations[0].instances[0]
#print instance
#key_path = os.path.join(os.path.expanduser('keys'),'Key-eu-west-1.pem')
#cmd = boto.manage.cmdshell.sshclient_from_instance(instance,key_path,user_name='ubuntu')
#print cmd
#print stopCassandra(cmd)
#print cleanCassandra(cmd)
#print updateCassandraYaml(cmd,['1.2.3.4','5.6.7.8','9.10.11.12'],'aa.bb.cc.dd','Ec2MultiRegionSnitch')

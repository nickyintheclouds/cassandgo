#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging,boto.manage.cmdshell
from aws import logError

#####################################################
# Execute a remote command on the boto shell server #
#####################################################

def runCmd(cmd,command):
        """
        run command on the server via ssh (cmd : boto.manage.cmdshell)
        """

        try:
                res = cmd.run(command)
                if res[2] != '':
                        raise Exception(res[2])
                return res
        except Exception as e:
                logError(e)
                return None

###########################
# DataStax Agent commands #
###########################

def updateDataStaxAgent(cmd,opsCenterIP):
        """
        Update the stomp_interface for the DataStax agent with the OpsCenter server ip
        """
        return runCmd(cmd,'echo "stomp_interface: '+opsCenterIP+'" | sudo tee /var/lib/datastax-agent/conf/address.yaml > /dev/null')

def startDataStaxAgent(cmd):
        """
        Start the DataStax agent
        """
        return runCmd(cmd,'sudo /etc/init.d/datastax-agent start')

def stopDataStaxAgent(cmd):
        """
        Stop the DataStax agent
        """
        return runCmd(cmd,'sudo /etc/init.d/datastax-agent stop')

####################
# OpsCenter Server #
####################

def startOpsCenter(cmd):
        """
        Start the OpsCenter server
        """
        return runCmd(cmd,'sudo /etc/init.d/opscenterd start')

def restartOpsCenter(cmd):
        """
        Start the OpsCenter server
        """
        return runCmd(cmd,'sudo /etc/init.d/opscenterd restart')

def stopOpsCenter(cmd):
        """
        Stop the OpsCenter server
        """
        return runCmd(cmd,'sudo /etc/init.d/opscenterd stop')

####################
# Cassandra Server #
####################

def startCassandra(cmd):
        """
        Start Cassandra server
        """
        return runCmd(cmd,'sudo /etc/init.d/cassandra start')

def stopCassandra(cmd):
        """
        Stop Cassandra server
        """
        return runCmd(cmd,'sudo /etc/init.d/cassandra stop')

def statusCassandra(cmd):
        """
        Cassandra server status
        """
        return runCmd(cmd,'sudo /etc/init.d/cassandra status')

def clusterStatus(cmd):
        """
        Get the current Cluster status
        """
        res = runCmd(cmd,'nodetool status')
        if res:
                return res[1]
        else:
                return ""

def cleanCassandra(cmd):
        """
        Empty the /var/lib/cassandra/*/* directories for a clean state
        """
        return runCmd(cmd,'sudo rm -rf /var/lib/cassandra/*/*')

def updateCassandraYaml(cmd,seeds,broadcast_addr,snitch):
        """
        Update the cassandra yaml file with the new seed servers, broadcast address and snitch type
        """

        # grab the original parameters
        grep_seeds = runCmd(cmd,"cat /etc/cassandra/cassandra.yaml | grep 'seeds:'")
        grep_broadcast = runCmd(cmd,"cat /etc/cassandra/cassandra.yaml | grep 'broadcast_address:'")
        grep_rpc = runCmd(cmd,"cat /etc/cassandra/cassandra.yaml | grep 'rpc_address:'")
        grep_snitch = runCmd(cmd,"cat /etc/cassandra/cassandra.yaml | grep 'endpoint_snitch:'")

        ip_seeds =  ' '*grep_seeds[1].index('-')+'- seeds: "'+','.join(seeds)+'"'

        # Backup of the original yaml file
        runCmd(cmd,'sudo cp /etc/cassandra/cassandra.yaml /etc/cassandra/cassandra_yaml.org')

        # Yaml sed processing
        command = 'sudo cat /etc/cassandra/cassandra.yaml | sed -e \'s/^'+grep_seeds[1].rstrip()+'/'+ip_seeds+'/g\' | sed -e \'s/^'+grep_broadcast[1].rstrip()+'/broadcast_address: "'+broadcast_addr+'"/g\' | sed -e \'s/^'+grep_rpc[1].rstrip()+'/rpc_address: 0.0.0.0/g\' | sed -e \'s/^'+grep_snitch[1].rstrip()+'/endpoint_snitch: '+snitch+'/g\' > /tmp/cassandra.yaml'
        runCmd(cmd,command)
        runCmd(cmd,'sudo cp /tmp/cassandra.yaml /etc/cassandra/cassandra.yaml')

        return True


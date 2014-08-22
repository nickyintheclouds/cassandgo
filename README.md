# CassAndGo

# In a nutshell

CassAndGo is a tool that allows you to quickly setup a multi DC Cassandra Cluster on Amazon EC2. It is based on DataStax Community AMIs. Really simple to use, it will speed up your tests and deployments.

Imagine you want to set up a 3 Datacenter Cassandra Cluster with 5 nodes (m3.large) in 3 regions (eu-west-1, us-east-1, us-west-1) and place your nodes in different availability zones (AZ) to benefit from the rack aware replication....

just add these settings (MultiDC) to your cassandgo.yaml :

```YAML
---
# Multi-DC configuration
MultiDC:
- datacenter: DC1
  region: eu-west
  zone: 1
  nodes: 5
  nb_seeds_per_dc: 2
  node_type: m3.large
  opscenter: yes

- datacenter: DC2
  region: us-east
  zone: 1
  nodes: 5
  nb_seeds_per_dc: 2
  node_type: m3.large
  opscenter: no

- datacenter: DC3
  region: us-west
  zone: 1
  nodes: 5
  nb_seeds_per_dc: 2
  node_type: m3.large
  opscenter: no
```

**in 10 minutes, you will get a fully functional multiDC Cassandra Cluster with OpsCenter and DataStax agents configured and all info to connect to your nodes and OpsCenter GUI !**

```console
./cassandgo.py create MultiDC
```

```gherkin
Cluster creation...
--------------------------------------------------------------------------------
Cluster MultiDC  in  eu-west-1  : 5  nodes [ m3.large ]  2  seed(s) opsCenter: True
Cluster MultiDC  in  us-east-1  : 5  nodes [ m3.large ]  2  seed(s) 
Cluster MultiDC  in  us-west-1  : 5  nodes [ m3.large ]  2  seed(s) 

Waiting for nodes...
--------------------------------------------------------------------------------
DC1 : Node 1 in eu-west-1a -> OK [107s] IP:54.216.130.151/10.98.131.6
DC1 : Node 2 in eu-west-1b -> OK [101s] IP:54.73.120.163/10.82.142.223
DC1 : Node 3 in eu-west-1c -> OK [96s] IP:54.216.50.81/10.105.176.118
DC1 : Node 4 in eu-west-1a -> OK [90s] IP:79.125.96.156/10.74.7.136
DC1 : Node 5 in eu-west-1b -> OK [84s] IP:54.220.37.219/10.36.53.34
DC2 : Node 1 in us-east-1a -> OK [77s] IP:54.204.160.177/10.147.18.55
DC2 : Node 2 in us-east-1c -> OK [71s] IP:54.89.233.129/10.179.187.29
DC2 : Node 3 in us-east-1d -> OK [66s] IP:54.198.144.116/10.179.169.244
DC2 : Node 4 in us-east-1a -> OK [60s] IP:54.167.25.122/10.51.147.135
DC3 : Node 2 in us-west-1c -> OK [40s] IP:54.183.170.1/172.31.4.83
DC2 : Node 5 in us-east-1c -> OK [58s] IP:54.89.214.78/10.136.53.115
DC3 : Node 4 in us-west-1c -> OK [35s] IP:54.183.131.231/172.31.7.191
DC3 : Node 3 in us-west-1a -> OK [54s] IP:54.183.182.144/172.31.28.202
DC3 : Node 5 in us-west-1a -> OK [44s] IP:54.183.146.107/172.31.27.190
DC3 : Node 1 in us-west-1a -> OK [73s] IP:54.183.154.163/172.31.26.107

Waiting for Cassandra warmup on all nodes ( 180 s)...
--------------------------------------------------------------------------------

Stopping Cassandra, opsCenter and Datastax agent on all nodes...
--------------------------------------------------------------------------------
DC1 : Node 1 in eu-west-1a
DC1 : Node 2 in eu-west-1b
DC1 : Node 3 in eu-west-1c
DC1 : Node 4 in eu-west-1a
DC1 : Node 5 in eu-west-1b
DC2 : Node 1 in us-east-1a
DC2 : Node 2 in us-east-1c
DC2 : Node 3 in us-east-1d
DC2 : Node 4 in us-east-1a
DC2 : Node 5 in us-east-1c
DC3 : Node 1 in us-west-1a
DC3 : Node 2 in us-west-1c
DC3 : Node 3 in us-west-1a
DC3 : Node 4 in us-west-1c
DC3 : Node 5 in us-west-1a

Cleaning cassandra data files on all nodes...
--------------------------------------------------------------------------------
DC1 : Node 1 in eu-west-1a
DC1 : Node 2 in eu-west-1b
DC1 : Node 3 in eu-west-1c
DC1 : Node 4 in eu-west-1a
DC1 : Node 5 in eu-west-1b
DC2 : Node 1 in us-east-1a
DC2 : Node 2 in us-east-1c
DC2 : Node 3 in us-east-1d
DC2 : Node 4 in us-east-1a
DC2 : Node 5 in us-east-1c
DC3 : Node 1 in us-west-1a
DC3 : Node 2 in us-west-1c
DC3 : Node 3 in us-west-1a
DC3 : Node 4 in us-west-1c
DC3 : Node 5 in us-west-1a
DC1 : Node 1 in eu-west-1a
DC1 : Node 2 in eu-west-1b
DC1 : Node 3 in eu-west-1c
DC1 : Node 4 in eu-west-1a
DC1 : Node 5 in eu-west-1b
DC2 : Node 1 in us-east-1a
DC2 : Node 2 in us-east-1c
DC2 : Node 3 in us-east-1d
DC2 : Node 4 in us-east-1a
DC2 : Node 5 in us-east-1c
DC3 : Node 1 in us-west-1a
DC3 : Node 2 in us-west-1c
DC3 : Node 3 in us-west-1a
DC3 : Node 4 in us-west-1c
DC3 : Node 5 in us-west-1a

Updating cassandra.yaml and DataStax agent conf on all nodes...
--------------------------------------------------------------------------------
DC1 : Node 1 in eu-west-1a
DC1 : Node 2 in eu-west-1b
DC1 : Node 3 in eu-west-1c
DC1 : Node 4 in eu-west-1a
DC1 : Node 5 in eu-west-1b
DC2 : Node 1 in us-east-1a
DC2 : Node 2 in us-east-1c
DC2 : Node 3 in us-east-1d
DC2 : Node 4 in us-east-1a
DC2 : Node 5 in us-east-1c
DC3 : Node 1 in us-west-1a
DC3 : Node 2 in us-west-1c
DC3 : Node 3 in us-west-1a
DC3 : Node 4 in us-west-1c
DC3 : Node 5 in us-west-1a

Starting Cassandra Seeds nodes...
--------------------------------------------------------------------------------
DC1 : Node 1 in eu-west-1a
DC1 : Node 2 in eu-west-1b
DC2 : Node 1 in us-east-1a
DC2 : Node 2 in us-east-1c
DC3 : Node 1 in us-west-1a
DC3 : Node 2 in us-west-1c

Starting Cassandra on all other nodes...
--------------------------------------------------------------------------------
DC1 : Node 3 in eu-west-1c
DC1 : Node 4 in eu-west-1a
DC1 : Node 5 in eu-west-1b
DC2 : Node 3 in us-east-1d
DC2 : Node 4 in us-east-1a
DC2 : Node 5 in us-east-1c
DC3 : Node 3 in us-west-1a
DC3 : Node 4 in us-west-1c
DC3 : Node 5 in us-west-1a

Starting OpsCenter...
--------------------------------------------------------------------------------
DC1 : Node 1 in eu-west-1

Starting DataStax Agents...
--------------------------------------------------------------------------------
DC1 : Node 1 in eu-west-1a
DC1 : Node 2 in eu-west-1b
DC1 : Node 3 in eu-west-1c
DC1 : Node 4 in eu-west-1a
DC1 : Node 5 in eu-west-1b
DC2 : Node 1 in us-east-1a
DC2 : Node 2 in us-east-1c
DC2 : Node 3 in us-east-1d
DC2 : Node 4 in us-east-1a
DC2 : Node 5 in us-east-1c
DC3 : Node 1 in us-west-1a
DC3 : Node 2 in us-west-1c
DC3 : Node 3 in us-west-1a
DC3 : Node 4 in us-west-1c
DC3 : Node 5 in us-west-1a

Cassandra cluster finalization...
--------------------------------------------------------------------------------

Intra-Cluster latencies...
--------------------------------------------------------------------------------
 ----------- 
|    DC1    | eu-west-1a <----> eu-west-1b : 0.96 ms
|===========| eu-west-1a <----> eu-west-1c : 0.89 ms
| eu-west-1 | eu-west-1b <----> eu-west-1c : 0.66 ms
 ----------- 
 ----------- 
|    DC2    | us-east-1a <----> us-east-1c : 0.97 ms
|===========| us-east-1a <----> us-east-1d : 1.64 ms
| us-east-1 | us-east-1c <----> us-east-1d : 0.66 ms
 ----------- 
 ----------- 
|    DC3    |
|===========| us-west-1a <----> us-west-1c : 1.43 ms
| us-west-1 |
 ----------- 

Inter-Cluster latencies...
--------------------------------------------------------------------------------
 -----------                  -----------                  -----------  
|    DC1    |                |    DC2    |                |    DC3    | 
|===========| <------------> |===========| <------------> |===========| 
| eu-west-1 |    85.62 ms    | us-east-1 |    83.27 ms    | us-west-1 | 
 -----------                  -----------                  -----------  

 -----------                                               -----------  
|    DC1    |                                             |    DC3    | 
|===========| <-----------------------------------------> |===========| 
| eu-west-1 |                  167.43 ms                  | us-west-1 | 
 -----------                                               -----------  


How to connect to MultiDC's nodes...
--------------------------------------------------------------------------------
[DC1] eu-west-1
--------------------------------------------------------------------------------
Node 1 : ssh -i keys/Key-eu-west-1.pem ubuntu@54.216.130.151
Node 2 : ssh -i keys/Key-eu-west-1.pem ubuntu@54.73.120.163
Node 3 : ssh -i keys/Key-eu-west-1.pem ubuntu@54.216.50.81
Node 4 : ssh -i keys/Key-eu-west-1.pem ubuntu@79.125.96.156
Node 5 : ssh -i keys/Key-eu-west-1.pem ubuntu@54.220.37.219

[DC2] us-east-1
--------------------------------------------------------------------------------
Node 1 : ssh -i keys/Key-us-east-1.pem ubuntu@54.204.160.177
Node 2 : ssh -i keys/Key-us-east-1.pem ubuntu@54.89.233.129
Node 3 : ssh -i keys/Key-us-east-1.pem ubuntu@54.198.144.116
Node 4 : ssh -i keys/Key-us-east-1.pem ubuntu@54.167.25.122
Node 5 : ssh -i keys/Key-us-east-1.pem ubuntu@54.89.214.78

[DC3] us-west-1
--------------------------------------------------------------------------------
Node 1 : ssh -i keys/Key-us-west-1.pem ubuntu@54.183.154.163
Node 2 : ssh -i keys/Key-us-west-1.pem ubuntu@54.183.170.1
Node 3 : ssh -i keys/Key-us-west-1.pem ubuntu@54.183.182.144
Node 4 : ssh -i keys/Key-us-west-1.pem ubuntu@54.183.131.231
Node 5 : ssh -i keys/Key-us-west-1.pem ubuntu@54.183.146.107


Connect to OpsCenter
--------------------------------------------------------------------------------
http://54.216.130.151:8888

Cluster status...
--------------------------------------------------------------------------------
Datacenter: eu-west
===================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address         Load       Tokens  Owns (effective)  Host ID                               Rack
UN  79.125.96.156   110.33 KB  256     13.4%             3b950b60-8229-434a-80f3-6c7bc03a6bd3  1a
UN  54.220.37.219   105.13 KB  256     13.2%             60b072cf-c357-4812-8cbc-d23fa53ac459  1b
UN  54.73.120.163   126.98 KB  256     13.7%             ca8aef3a-fac7-4642-8a5c-b493a9b8365b  1b
UN  54.216.50.81    105.96 KB  256     13.1%             079fa6bf-3660-44e4-beb4-9bc4510c904e  1c
UN  54.216.130.151  105.65 KB  256     13.0%             80d06ee4-1594-4c12-8fbe-a6996ae4d3ee  1a
Datacenter: us-west
===================
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address         Load       Tokens  Owns (effective)  Host ID                               Rack
UN  54.183.182.144  161.51 KB  256     12.8%             098a7ffa-2022-4f07-af95-2770c0eaf90a  1a
UN  54.183.170.1    130.62 KB  256     12.7%             527c2d73-9cdf-48e9-b6a8-087ff8e7361f  1c
UN  54.183.146.107  130.59 KB  256     14.2%             c08547f8-d049-4033-8699-400ac35e7ea9  1a
UN  54.183.131.231  149.81 KB  256     14.2%             392a3407-df5a-4750-8984-0f0bd3ccc441  1c
UN  54.183.154.163  140.4 KB   256     13.1%             895c28bc-3821-4fb5-9862-9c75d79412ae  1a
Datacenter: us-east
===================
Status/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address         Load       Tokens  Owns (effective)  Host ID                               Rack
UN  54.89.233.129   115.46 KB  256     13.4%             371f35ec-7641-45fc-8ec3-986e48c7ef73  1c
UN  54.167.25.122   120.46 KB  256     12.7%             9f90996d-cdd7-425e-96c0-f83135ff5b24  1a
UN  54.198.144.116  125.37 KB  256     12.7%             a6cebd90-709a-4bb1-ae45-6185d006ff42  1d
UN  54.204.160.177  124.74 KB  256     13.7%             b48b590a-74c6-469f-8547-3170d6717bf2  1a
UN  54.89.214.78    100.88 KB  256     14.1%             85340e57-199c-4de4-b620-a45d4f139183  1c

```

Et voilà ! :-)

# Install

**Install python (2.5, 2.6, or 2.7)**
To check if it is installed just type "python -V" in a terminal window
In the unlikely event it's not already installed you can simply install it with your OSes package manager.

```console
$ python -V
Python 2.7.6
```
This tool use the excellent [boto](https://github.com/boto) library to access Amazon Web Services.
```console
$ pip install boto
```
To access your AWS account, you need to enter your Amazon credentials in the ~/.boto file :

```console
$ vi ~/.boto
```

```INI
[Credentials]
aws_access_key_id = XXXXXXXXXXXXXXXX
aws_secret_access_key = YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
```

# Initial setup

The CassAndGo tool uses specific Security Groups and Key Pairs on the different Amazon regions. These entities have to be created once before attempting to deploy any cassandra cluster :

## Security Groups

The name of these security groups is based on the following template :

**name = SG-Cassandra-[region]-[zone]**

```console
$ ./cassandgo.py initSG
```

```console
Creating SG-Cassandra-us-east-1 Security Group
Creating SG-Cassandra-us-west-1 Security Group
Creating SG-Cassandra-us-west-2 Security Group
Creating SG-Cassandra-eu-west-1 Security Group
Creating SG-Cassandra-ap-southeast-1 Security Group
Creating SG-Cassandra-ap-southeast-2 Security Group
Creating SG-Cassandra-ap-northeast-1 Security Group
Creating SG-Cassandra-sa-east-1 Security Group
```

## Key pairs

All key pair **.pem** files will be stored in a '**keys**' subdirectory :

**name = Key-[region]-[zone]**

```console
$ ./cassandgo.py initKP
```

```console
Key creation : Key-us-east-1
Key creation : Key-us-west-1
Key creation : Key-us-west-2
Key creation : Key-eu-west-1
Key creation : Key-ap-southeast-1
Key creation : Key-ap-southeast-2
Key creation : Key-ap-northeast-1
Key creation : Key-sa-east-1
```

```console
$ ls -alg keys

total 64
drwxr-xr-x  10 staff   340 22 aoû 11:16 .
drwxr-xr-x  15 staff   510 22 aoû 00:37 ..
-rw-------   1 staff  1670 22 aoû 11:16 Key-ap-northeast-1.pem
-rw-------   1 staff  1670 22 aoû 11:15 Key-ap-southeast-1.pem
-rw-------   1 staff  1674 22 aoû 11:15 Key-ap-southeast-2.pem
-rw-------   1 staff  1674 22 aoû 11:15 Key-eu-west-1.pem
-rw-------   1 staff  1674 22 aoû 11:16 Key-sa-east-1.pem
-rw-------   1 staff  1670 22 aoû 11:15 Key-us-east-1.pem
-rw-------   1 staff  1674 22 aoû 11:15 Key-us-west-1.pem
-rw-------   1 staff  1674 22 aoû 11:15 Key-us-west-2.pem
```

# Create your first Cluster

Once all Security groups, Key pairs and boto credentials have been configured, you could now launch your MultiDC Cassandra Cluster by editing the cassandgo.yaml file :

```YAML
---
# Multi-DC configuration

MonoDC:
- datacenter: DC1
  region: eu-west
  zone: 1
  nodes: 6
  nb_seeds_per_dc: 2
  node_type: m3.large
  opscenter: yes
  
MultiDC:
- datacenter: DC1
  region: eu-west
  zone: 1
  nodes: 5
  nb_seeds_per_dc: 2
  node_type: m3.large
  opscenter: yes

- datacenter: DC2
  region: us-east
  zone: 1
  nodes: 5
  nb_seeds_per_dc: 2
  node_type: m3.large
  opscenter: no

- datacenter: DC3
  region: us-west
  zone: 1
  nodes: 5
  nb_seeds_per_dc: 2
  node_type: m3.large
  opscenter: no
```

As you can see, you could define numerous Cluster configuration (ie: MonoDC, MultiDC)
For each conf, you have to list all Datacenters involved and their settings :


- region
- zone
- nodes
- nb_seeds_per_dc (among all nodes, how many will be seed nodes, 2 is a good value for redundancy in case of a seed node crash)
- node_type (Amazon instance type)
- opscenter (if yes, the first node of this DC will provide a opsCenter server and all DataStax agents from other nodes will point to it)


> **WARNING** : It is not recommended to activate more than one OpsCenter Server in your cluster, for example opscenter set to yes in all Datacenters. Just set only one and leave all other opscenters to no in other DCs.

Now, you can deploy your cluster :

```console
$ ./cassandgo.py create MultiDC
```

> **WARNING** : During the cluster creation, the tool connects to node via ssh and then **ssh fingerprints** are automatically added to your **.ssh/known_hosts** file. If you create, destroy many clusters, you could then have conflicts with these previous fingerprints. A good tip is to clean previous ec2 IPs from your .ssh/known_hosts file before creating your cluster.

# Destroy a Cluster

If you want to terminate all instances of your cluster (and stop billing :-), just type the following command with the name of your cluster :

```console
$ ./cassandgo.py destroy MultiDC
```

# Test the cluster

Once your cluster created, you could check the replication across the Amazon regions by tracing on a INSERT operation :

First, we have to connect for example to our first node in the first DC (see the **How to connect section** in the creation output)

```console
ssh -i keys/Key-eu-west-1.pem ubuntu@54.216.130.151
```

then, we will init our keyspace with a **NetworkTopology strategy** and a **replication factor RF = 3** :

```console
cqlsh

cqlsh> CREATE KEYSPACE "NetworkTopologyStratRF3RF3RF3" WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'eu-west' : 3, 'us-east' : 3, 'us-west' : 3};

cqlsh> use multidckeyspace ;
```

We could check our newly keyspace in the system tables :
```console
cqlsh:multidckeyspace> select * from system.schema_keyspaces ;

 keyspace_name   | durable_writes | strategy_class                                       | strategy_options
-----------------+----------------+------------------------------------------------------+---------------------------------------------
       OpsCenter |           True |          org.apache.cassandra.locator.SimpleStrategy |                  {"replication_factor":"2"}
 multidckeyspace |           True | org.apache.cassandra.locator.NetworkTopologyStrategy | {"us-west":"3","eu-west":"3","us-west":"3"}
          system |           True |           org.apache.cassandra.locator.LocalStrategy |                                          {}
   system_traces |           True |          org.apache.cassandra.locator.SimpleStrategy |                  {"replication_factor":"2"}

(4 rows)

```

Now, let's create a simple **test** table :
```console
cqlsh:multidckeyspace> CREATE TABLE test (id bigint, msg text,PRIMARY KEY ((id)));
```

By setting **TRACING ON**, we will verbose all operations on the cluster and see that a simple INSERT is in fact, very active ! 

```console
cqlsh:multidckeyspace> TRACING ON
Now tracing requests.
cqlsh:multidckeyspace> INSERT INTO test (id, msg) VALUES (1,'All over the World !');

Tracing session: e030d950-29d8-11e4-9ad4-6f3f0fef8b26

 activity                                                              | timestamp    | source         | source_elapsed
-----------------------------------------------------------------------+--------------+----------------+----------------
                                                    execute_cql3_query | 08:46:57,895 | 54.216.130.151 |              0
                                 Message received from /54.183.146.107 | 08:46:57,836 |   54.183.170.1 |             75
                                        Acquiring switchLock read lock | 08:46:57,837 |   54.183.170.1 |           1201
                                                Appending to commitlog | 08:46:57,837 |   54.183.170.1 |           1254
                                               Adding to test memtable | 08:46:57,838 |   54.183.170.1 |           1340
                                 Enqueuing response to /54.216.130.151 | 08:46:57,838 |   54.183.170.1 |           1673
                                    Sending message to /54.216.130.151 | 08:46:57,838 |   54.183.170.1 |           1965
                                 Message received from /54.216.130.151 | 08:46:57,857 |   54.216.50.81 |             60
                                        Acquiring switchLock read lock | 08:46:57,858 |   54.216.50.81 |           1005
                                                Appending to commitlog | 08:46:57,858 |   54.216.50.81 |           1076
                                               Adding to test memtable | 08:46:57,858 |   54.216.50.81 |           1171
                                 Enqueuing response to /54.216.130.151 | 08:46:57,858 |   54.216.50.81 |           1457
                                       Sending message to /10.98.131.6 | 08:46:57,859 |   54.216.50.81 |           2032
 Parsing INSERT INTO test (id, msg) VALUES (1,'All over the World !'); | 08:46:57,895 | 54.216.130.151 |            836
                                                   Preparing statement | 08:46:57,896 | 54.216.130.151 |           1762
                                     Determining replicas for mutation | 08:46:57,896 | 54.216.130.151 |           1921
                                       Sending message to /10.74.7.136 | 08:46:57,897 | 54.216.130.151 |           2566
                                    Sending message to /10.105.176.118 | 08:46:57,897 | 54.216.130.151 |           2566
                                       Sending message to /10.36.53.34 | 08:46:57,897 | 54.216.130.151 |           2819
                                    Sending message to /54.183.146.107 | 08:46:57,898 | 54.216.130.151 |           2995
                                 Message received from /54.216.130.151 | 08:46:57,901 |  54.220.37.219 |             65
                                        Acquiring switchLock read lock | 08:46:57,902 |  54.220.37.219 |           1003
                                                Appending to commitlog | 08:46:57,902 |  54.220.37.219 |           1035
                                               Adding to test memtable | 08:46:57,902 |  54.220.37.219 |           1112
                                 Enqueuing response to /54.216.130.151 | 08:46:57,902 |  54.220.37.219 |           1352
                                       Sending message to /10.98.131.6 | 08:46:57,902 |  54.220.37.219 |           1583
                                 Message received from /54.216.130.151 | 08:46:57,904 |  79.125.96.156 |             76
                                        Acquiring switchLock read lock | 08:46:57,905 |  79.125.96.156 |           1148
                                                Appending to commitlog | 08:46:57,905 |  79.125.96.156 |           1182
                                               Adding to test memtable | 08:46:57,905 |  79.125.96.156 |           1267
                                 Enqueuing response to /54.216.130.151 | 08:46:57,905 |  79.125.96.156 |           1600
                                       Sending message to /10.98.131.6 | 08:46:57,906 |  79.125.96.156 |           1870
                                   Message received from /54.89.214.78 | 08:46:57,933 | 54.204.160.177 |            115
                                        Acquiring switchLock read lock | 08:46:57,934 | 54.204.160.177 |           1434
                                                Appending to commitlog | 08:46:57,934 | 54.204.160.177 |           1515
                                               Adding to test memtable | 08:46:57,934 | 54.204.160.177 |           1589
                                 Enqueuing response to /54.216.130.151 | 08:46:57,935 | 54.204.160.177 |           1882
                                    Sending message to /54.216.130.151 | 08:46:57,935 | 54.204.160.177 |           2133
                                   Message received from /54.89.214.78 | 08:46:57,938 | 54.198.144.116 |             64
                                        Acquiring switchLock read lock | 08:46:57,939 | 54.198.144.116 |           1044
                                                Appending to commitlog | 08:46:57,939 | 54.198.144.116 |           1071
                                               Adding to test memtable | 08:46:57,939 | 54.198.144.116 |           1152
                                 Enqueuing response to /54.216.130.151 | 08:46:57,939 | 54.198.144.116 |           1417
                                    Sending message to /54.216.130.151 | 08:46:57,939 | 54.198.144.116 |           1669
                                 Message received from /54.216.130.151 | 08:46:57,942 |   54.89.214.78 |             64
                          Enqueuing forwarded write to /54.204.160.177 | 08:46:57,943 |   54.89.214.78 |           1132
                          Enqueuing forwarded write to /54.198.144.116 | 08:46:57,943 |   54.89.214.78 |           1200
                                        Acquiring switchLock read lock | 08:46:57,943 |   54.89.214.78 |           1258
                                                Appending to commitlog | 08:46:57,943 |   54.89.214.78 |           1298
                                               Adding to test memtable | 08:46:57,943 |   54.89.214.78 |           1358
                                 Enqueuing response to /54.216.130.151 | 08:46:57,944 |   54.89.214.78 |           1666
                                    Sending message to /54.216.130.151 | 08:46:57,944 |   54.89.214.78 |           1867
                                      Sending message to /10.147.18.55 | 08:46:57,944 |   54.89.214.78 |           1869
                                    Sending message to /10.179.169.244 | 08:46:57,944 |   54.89.214.78 |           null
                                 Message received from /54.216.130.151 | 08:46:57,974 | 54.183.146.107 |             68
                          Enqueuing forwarded write to /54.183.131.231 | 08:46:57,975 | 54.183.146.107 |           1169
                            Enqueuing forwarded write to /54.183.170.1 | 08:46:57,975 | 54.183.146.107 |           1228
                                        Acquiring switchLock read lock | 08:46:57,975 | 54.183.146.107 |           1313
                                                Appending to commitlog | 08:46:57,975 | 54.183.146.107 |           1355
                                               Adding to test memtable | 08:46:57,975 | 54.183.146.107 |           1403
                                      Sending message to /172.31.7.191 | 08:46:57,975 | 54.183.146.107 |           1407
                                 Enqueuing response to /54.216.130.151 | 08:46:57,975 | 54.183.146.107 |           1716
                                 Message received from /54.183.146.107 | 08:46:57,976 | 54.183.131.231 |             58
                                       Sending message to /172.31.4.83 | 08:46:57,976 | 54.183.146.107 |           1779
                                    Sending message to /54.216.130.151 | 08:46:57,976 | 54.183.146.107 |           2007
                                        Acquiring switchLock read lock | 08:46:57,977 | 54.183.131.231 |            977
                                                Appending to commitlog | 08:46:57,977 | 54.183.131.231 |           1022
                                               Adding to test memtable | 08:46:57,977 | 54.183.131.231 |           1098
                                 Enqueuing response to /54.216.130.151 | 08:46:57,978 | 54.183.131.231 |           1345
                                    Sending message to /54.216.130.151 | 08:46:57,978 | 54.183.131.231 |           1582
                                                      Request complete |           -- | 54.216.130.151 |             --

cqlsh:multidckeyspace> TRACING OFF
Disabled tracing.
```



## Thanks


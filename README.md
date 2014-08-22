# CassAndGo

# In a nutshell

CassAndGo is a tool that allows you to quickly setup a multi DC Cassandra Cluster on Amazon EC2. It is based on DataStax Community AMIs
This tool is really simple to use and will speed up your tests and deployments.

Imagine you want to set up a 3 Datacenter Cassandra Cluster with 5 nodes (m3.large) in 3 regions (eu-west-1, us-east-1, us-west-1) and place your nodes in different availability zones (AZ) to benefit from the rack aware replication....

It is really simple, just add these settings to your cassandgo.yaml :

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

# Install

## boto

```console
$ pip install boto
```

and here is the result :

```gherkin

./cassandgo.py create MultiDC

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
bOpsCenterExists :  True

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
Status=Up/Down
|/ State=Normal/Leaving/Joining/Moving
--  Address         Load       Tokens  Owns (effective)  Host ID                               Rack
UN  54.89.233.129   115.46 KB  256     13.4%             371f35ec-7641-45fc-8ec3-986e48c7ef73  1c
UN  54.167.25.122   120.46 KB  256     12.7%             9f90996d-cdd7-425e-96c0-f83135ff5b24  1a
UN  54.198.144.116  125.37 KB  256     12.7%             a6cebd90-709a-4bb1-ae45-6185d006ff42  1d
UN  54.204.160.177  124.74 KB  256     13.7%             b48b590a-74c6-469f-8547-3170d6717bf2  1a
UN  54.89.214.78    100.88 KB  256     14.1%             85340e57-199c-4de4-b620-a45d4f139183  1c


```

## Thanks


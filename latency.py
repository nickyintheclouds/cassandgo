#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,logging,boto.manage.cmdshell, re
from aws import logError

def getLatency(cmd,toIP):
    """
    Ping latency average between fromDC and toDC
    """
    try:
        res = cmd.run('sudo ping -c3 '+toIP)
        m = re.search(' = [^\/]+\/([^\/]+)\/.+ ms',res[1])
        if m:
            return "%.2f ms" % round(float(m.group(1)),2)
    except Exception as e:
        logError(e)
    return ''

def boxWidth(cluster):
    """
    Width of the DC info box
     -----------
    |    DC2    |
    |===========|
    | eu-west-1 |
     -----------
    """
    width = len(cluster['datacenter'])
    w = len(cluster['region']+'-'+cluster['zone'])
    if w > width:   width = w

    # +4 for the padding and the border
    return (width+4)

def getLatencyAZ(cmd,toIP,fromAZ,toAZ):
    """
    Display latency between Availability Zones AZ
    """
    return fromAZ + ' <----> ' + toAZ + ' : ' + getLatency(cmd,toIP)

def getLatenciesRegion(cluster):
    """
    Display latencies within the same DC between AZ
    """
    # List of all AZs form this cluster
    AZInfo = {}
    AZs = []
    for instance in cluster['instances']:
        if (instance['AZ'] not in AZInfo):
            AZInfo[instance['AZ']] = {'instance':instance['instance'],'AZ':instance['AZ']}
            AZs.append(instance['AZ'])

    lines = ['','','','','','']
    for ln in range(5): lines[ln] = boxPart(cluster,ln+1)
    key_path = os.path.join(os.path.expanduser('keys'),'Key-'+cluster['region']+'-'+cluster['zone']+'.pem')

    if len(AZs) == 2:
        cmd = boto.manage.cmdshell.sshclient_from_instance(AZInfo[AZs[0]]['instance'],key_path,user_name='ubuntu')
        for i in (0,1):   print lines[i]
        print lines[2] + ' ' + getLatencyAZ(cmd,AZInfo[AZs[1]]['instance'].private_ip_address,AZInfo[AZs[0]]['AZ'],AZInfo[AZs[1]]['AZ'])
        for i in (3,4):   print lines[i]
    elif len(AZs) >= 3:
        cmd1 = boto.manage.cmdshell.sshclient_from_instance(AZInfo[AZs[0]]['instance'],key_path,user_name='ubuntu')
        cmd2 = boto.manage.cmdshell.sshclient_from_instance(AZInfo[AZs[1]]['instance'],key_path,user_name='ubuntu')
        print lines[0]
        print lines[1] + ' ' + getLatencyAZ(cmd1,AZInfo[AZs[1]]['instance'].private_ip_address,AZInfo[AZs[0]]['AZ'],AZInfo[AZs[1]]['AZ'])
        print lines[2] + ' ' + getLatencyAZ(cmd1,AZInfo[AZs[2]]['instance'].private_ip_address,AZInfo[AZs[0]]['AZ'],AZInfo[AZs[2]]['AZ'])
        print lines[3] + ' ' + getLatencyAZ(cmd2,AZInfo[AZs[2]]['instance'].private_ip_address,AZInfo[AZs[1]]['AZ'],AZInfo[AZs[2]]['AZ'])
        print lines[4]
    else:
        print lines[0]
        print lines[1] + ' ' + AZInfo[AZs[0]]['AZ']
        for i in (2,3,4):   print lines[i]

def boxPart(cluster,line):
    """
    ASCII drawing of the DC info box for a specific line
     -----------
    |    DC2    |
    |===========|
    | eu-west-1 |
     -----------
    """
    width = boxWidth(cluster)
    if ((line == 1) or (line == 5)):
        return ' '+'-'*(width-2)+' '
    elif line == 2:
        leftGap = int(((width-4)-len(cluster['datacenter']))/2)
        rightGap = (width-4) - leftGap - len(cluster['datacenter'])
        return '| '+' '*leftGap+cluster['datacenter']+' '*rightGap+' |'
    elif line == 3:
        return '|'+'='*(width-2)+'|'
    elif line == 4:
        leftGap = int(((width-4)-len(cluster['region']+'-'+cluster['zone']))/2)
        rightGap = (width-4) - leftGap - len(cluster['region']+'-'+cluster['zone'])
        return '| '+' '*leftGap+cluster['region']+'-'+cluster['zone']+' '*rightGap+' |'
    else:
        return ""

def getDCIdx(clusters,dc):
    """
    get the index of the dc in the clusters List
    """
    idx = 0
    for cluster in clusters:
        if (cluster['datacenter'] == dc):
            return idx
        idx += 1
    return -1

def printLatency(clusters,dcs):
    """
    Display latency average between different DCS
    """
    arrowWidth = 12
    leftArrow = '<'
    rightArow = '>'

    lines = ['','','','','']
    i = 0
    while (i<len(dcs)):
        idxStart = getDCIdx(clusters,dcs[i])
        key_path = os.path.join(os.path.expanduser('keys'),'Key-'+clusters[idxStart]['region']+'-'+clusters[idxStart]['zone']+'.pem')
        cmd = boto.manage.cmdshell.sshclient_from_instance(clusters[idxStart]['instances'][0]['instance'],key_path,user_name='ubuntu')
        if i == 0:
            for ln in range(5): lines[ln] = boxPart(clusters[idxStart],ln+1) + ' '
        else:
            for ln in range(5): lines[ln] += ' '
        i += 1
        if (i < len(dcs)):
            idxEnd = getDCIdx(clusters,dcs[i])
            ip = clusters[idxEnd]['instances'][0]['instance'].ip_address
            gap = 0
            j = idxStart+1
            while (j < idxEnd):
                gap += len(leftArrow)+len(rightArow)+2+boxWidth(clusters[j])
                j += 1
            arrow = leftArrow + '-' * (arrowWidth*(idxEnd-idxStart) + gap) + rightArow
            for ln in (0,1,4):  lines[ln] += ' '*len(arrow) + ' ' + boxPart(clusters[idxEnd],ln+1)
            lines[2] += arrow + ' ' + boxPart(clusters[idxEnd],3)
            latency = getLatency(cmd,ip)
            leftGap = int((len(arrow)-len(latency))/2)
            rightGap = len(arrow) - leftGap - len(latency)
            lines[3] += ' '*leftGap + latency + ' '*rightGap + ' ' + boxPart(clusters[idxEnd],4)

    for ln in range(5): print lines[ln]

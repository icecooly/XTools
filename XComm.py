#!/usr/bin/python
#-*-coding:utf-8-*-

import os
import sys
import re
from Host import *

def getHosts():
    xtoolsHome=os.environ.get('XTOOLS_HOME')
    if xtoolsHome is None:
        logError("please set up XTOOLS_HOME in .bashrc");
        sys.exit(-1)
    result = list()
    fileName=xtoolsHome + os.path.sep + "hosts.txt"
    print('%s'%fileName)
    f=open(fileName, 'r');
    for host in f.readlines(): 
        host = host.strip()  
        if not len(host) or host.startswith('#'): 
            continue  
        content = re.split(' |\t', host);
        content = [item for item in filter(lambda x: x != '', content)] 
        if len(content) != 5:
            logError('error host:%s'%host)
            continue
        newHost=Host(content[0].strip(),content[1].strip(),content[2].strip(),content[3].strip(),content[4].strip())
        result.append(newHost)
    f.close()
    return result

def getHostByAlias(alias):
    hosts=getHosts()
    for host in hosts:
        if host.alias==alias:
            return host
    logError('host not found alias:%s'%alias)
    sys.exit(-1)

def getHostsByAlias(alias):
    hosts = getHosts()
    result=list()
    for host in hosts:
        if re.match(alias,host.alias):
            result.append(host)
    if len(result)==0:
        logError('host not found alias:%s' % alias)
        sys.exit(-1)
    return result

def printHosts():
    hosts=getHosts()
    logInfo("hosts:")
    for host in hosts:
        logInfo(host)


def logWarnning(msg):
    print("\033[33m"+msg+"\033[0m")

def logError(msg):
    print("\033[31m" + msg + "\033[0m")

def logDebug(msg):
    print("\033[32m" + msg + "\033[0m")

def logInfo(msg):
    print(msg)


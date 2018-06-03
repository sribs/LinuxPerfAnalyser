import os
import time
import multiprocessing
from datetime import datetime as dt
import sys
import argparse
import math

def memory(t=10,i=1,**kwargs):
    jiffy = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
    memTotal=int(open('/proc/meminfo').readlines()[0].split(':')[1].strip().strip(' kB'))*1000
    swapTotal=int(open('/proc/meminfo').readlines()[14].split(':')[1].strip().strip(' kB'))*1000
    memTotall=[memTotal for x in range(int(math.ceil(t/i)))]
    swapTotall=[swapTotal for x in range(int(math.ceil(t/i)))]
    memUsedl=[]
    memFreel=[]
    buffersl=[]
    cachedMl=[]
    nonCachedl=[]
    swapl=[]
    date=[]

    for x in range(int(math.ceil(t/i))):
        mem=open('/proc/meminfo')
        meminfo=mem.readlines()
        date.append(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
        memFree=int(meminfo[1].split(':')[1].strip().strip(' kB'))*1000
        memUsed=memTotal-memFree
        buffers=int(meminfo[3].split(':')[1].strip().strip(' kB'))*1000
        cachedM=int(meminfo[4].split(':')[1].strip().strip(' kB'))*1000+int(meminfo[22].split(':')[1].strip().strip(' kB'))*1000-1000*int(meminfo[20].split(':')[1].strip().strip(' kB'))
        nonCached=memUsed-(cachedM+buffers)
        swap=swapTotal-int(meminfo[15].split(':')[1].strip().strip(' kB'))*1000
        memFreel.append(memFree)
        memUsedl.append(memUsed)
        buffersl.append(buffers)
        cachedMl.append(cachedM)
        nonCachedl.append(nonCached)
        swapl.append(swap)
        time.sleep(i)
        mem.close()
    
    jsfile=open("memory.js","w+")
    jsfile.write("""
    var memTotal={{'x':{0},'y':{1},'type':'scatter','name':'Total memory kB'}};
    var memUsed={{'x':{2},'y':{3},'type':'scatter','name':'Memory Used kB'}};
    var memFree={{'x':{4},'y':{5},'type':'scatter','name':'Memory Free kB'}};
    var NonCached={{'x':{0},'y':{6},'type':'scatter','name':'NonCached kB'}};
    var buffers={{'x':{2},'y':{7},'type':'scatter','name':'buffers kB'}};
    var cachedM={{'x':{4},'y':{8},'type':'scatter','name':'Cacled kB'}};
    var memData=[memTotal,memUsed,memFree,NonCached,buffers,cachedM]; var memlayout = {{
    title:'Memory Usage Line Graph'
    }};
    var swapTotal={{'x':{2},'y':{9},'type':'scatter','name':'swapTotal kB'}};
    var swapUsed={{'x':{4},'y':{10},'type':'scatter','name':'swapUsed kB'}};
    var swapData=[swapTotal,swapUsed]; 
    var swaplayout = {{
    title:'Swap Usage Line Graph'
    }};""".format(date,memTotall,date,memUsedl,date,memFreel,nonCachedl,buffersl,cachedMl,swapTotall,swapl))
    
memory()






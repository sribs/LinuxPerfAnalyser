import os
import time
import multiprocessing
from datetime import datetime as dt
import sys
import argparse
import math

def cpuUsage(t=10,i=1,**kwargs):
    jiffy = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
    num_cpu = multiprocessing.cpu_count()
    date=[]
    userl=[]
    systeml=[]
    idlel=[]
    nicel=[]
    iowaitl=[]
    irql=[]


    stat_fd = open('/proc/stat')
    stat_buf = stat_fd.readlines()[0].split()
    user, nice, system, idle, iowait, irq, sirq = ( float(stat_buf[1]), float(stat_buf[2]),
                                            float(stat_buf[3]), float(stat_buf[4]),
                                            float(stat_buf[5]), float(stat_buf[6]),
                                            float(stat_buf[7]) )

    stat_fd.close()
    for x in range(int(math.ceil(t/i))):
        time.sleep(i)

        stat_fd = open('/proc/stat')
        stat_buf = stat_fd.readlines()[0].split()
        user_n, nice_n, sys_n, idle_n, iowait_n, irq_n, sirq_n = ( float(stat_buf[1]), float(stat_buf[2]),
                                                                float(stat_buf[3]), float(stat_buf[4]),
                                                                float(stat_buf[5]), float(stat_buf[6]),
                                                                float(stat_buf[7]) )

        stat_fd.close()
        date.append(dt.now().strftime("%Y-%m-%d %H:%M:%S"))
        systeml.append(((sys_n - system) * 100 / jiffy / i) / num_cpu)
        userl.append(((user_n - user) * 100 / jiffy / i) / num_cpu)
        idlel.append(((idle_n - idle) * 100 / jiffy / i) / num_cpu)
        nicel.append(((nice_n - nice) * 100 / jiffy / i) / num_cpu)
        iowaitl.append(((iowait_n - iowait) * 100 / jiffy / i) / num_cpu)
        irql.append(((irq_n - irq) * 100 / jiffy / i) / num_cpu)
        user=user_n
        system=sys_n
        idle=idle_n
        iowait=iowait_n
        nice=nice_n
        irq=irq_n
    
    jsfile=open("cpu.js","w+")
    jsfile.write("""var usercpu={{'x':{0},'y':{1},'type':'scatter','name':'User%'}};
    var syscpu={{
    'x':{2},'y':{3},'type':'scatter','name':'System%'}};
    var idlecpu={{
    'x':{4},'y':{5},'type':'scatter','name':'Idle%'}};
    var nice={{'x':{0},'y':{6},'type':'scatter','name':'Nice%'}};
    var iowait={{
    'x':{2},'y':{7},'type':'scatter','name':'iowait%'}};
    var irq={{
    'x':{4},'y':{8},'type':'scatter','name':'Interrupts/s%'}};
    var data=[usercpu,syscpu,idlecpu,nice,iowait,irq]; var layout = {{
    title:'CPU Usage Line Graph'
    }};""".format(date,userl,date,systeml,date,idlel,nicel,iowaitl,irql))

    #jsfile.write("""var usercpu=\{{ x:{{0}},\y:{{1}},type:'scatter',name:'User%'\}}; var syscpu=\{{ x:{{0}},y:{{2}},type:'scatter',name:'System%'\}}; var idlecpu=\{{ x:{{0}},y:{{3}},type:'scatter',name:'Idle%'\}};var data = [usercpu,syscpu,idlecpu];""".format(date,userl,systeml,idlel))




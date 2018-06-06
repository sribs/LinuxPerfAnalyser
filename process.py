import subprocess
import csv
from StringIO import StringIO

def Top10ProcessesMemory():
    """
    """
    p=subprocess.Popen("ps -eo user,cmd,%mem --sort=-%mem | head -n 5",shell=True,stdout=subprocess.PIPE)   
    q=subprocess.Popen("ps -eo user,cmd,%cpu --sort=-%cpu | head -n 5",shell=True,stdout=subprocess.PIPE) 
    memory = p.communicate()[0]
    cpu = q.communicate()[0]
    memory = memory.strip(" ")
    cpu = cpu.strip(" ")
    f = StringIO(memory)
    f1 = StringIO(cpu)
    i=0
    values=[]
    label=[]
    valuesCpu=[]
    labelCpu=[]
    memoryReader = csv.reader(f, delimiter=' ',skipinitialspace=True)
    for row in memoryReader:
        if(i==0):
            i+=1
            continue
        else:
            label.append('{0} {1}'.format(row[0],row[1]))
            values.append(float(row[-1]))
    print values,label
    i=0
    cpuReader = csv.reader(f1, delimiter=' ',skipinitialspace=True)
    for row in cpuReader:
        if(i==0):
            i+=1
            continue
        else:
            labelCpu.append('{0} {1}'.format(row[0],row[1]))
            valuesCpu.append(float(row[-1]))
    
    jsfile=open("process.js","w+")
    jsfile.write("""
    var procMemory=[{{
    values: {0},
    labels: {1},
    type: 'pie'
    }}];
    
    var procCPU=[{{
    values: {2},
    labels: {3},
    type: 'pie'
    }}];
    
    var layoutMemory = {{
        width:500,
        height:400,
        title:'Top 5 Process Consumers (Memory)'
    }};
    var layoutCPU = {{
        width:500,
        height:400,
        title:'Top 5 Process Consumers (CPU)'
    }};""".format(values,label,valuesCpu,labelCpu))
    jsfile.close()

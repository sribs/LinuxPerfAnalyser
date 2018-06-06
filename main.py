from cpu import cpuUsage
from memSwap import memory
import argparse
from process import Top10ProcessesMemory

def main(t=10,i=1,**kwargs):
    import threading
    cputhread = threading.Thread(target=cpuUsage,args=(t,i))
    memSwapthread = threading.Thread(target=memory,args=(t,i))
    cputhread.start()
    memSwapthread.start()
    cputhread.join()
    memSwapthread.join()
    Top10ProcessesMemory()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='CPU, Memory benchmark Tester')
    parser.set_defaults(method=main)
    parser.add_argument('-t','-time',type=int)
    parser.add_argument('-i','-interval',type=int)
    args=parser.parse_args()
    args.method(**vars(args))

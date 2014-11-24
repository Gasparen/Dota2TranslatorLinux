import psutil
import pcap
import sniff
import sys
import time

executableName = "dota_linux"

def getPort():
    for p in psutil.process_iter():
        if (p.name() == executableName):
            for c in p.connections():
                if c.status == 'NONE': # Status NONE is _obviously_ the one :S
                    return c.laddr[1]  # laddr = (ip-address, port)

def setupPort(port):
    p = pcap.pcapObject()
    dev = "eth0"
    net, mask = pcap.lookupnet(dev)
    p.open_live(dev, 1600, 0, 100)
    filterString = "port " + str(port)
    p.setfilter(filterString, 0, 0)
    return p

def timeDiff(lastScan, t):
    return int((t-lastScan) * 10)

# Taken from sniff.py in pylibpcap
def main():
    lastScan = time.clock()
    detectPort = True
    try:
        while 1:
            now = time.clock()
            if (timeDiff(lastScan, now) > 10):
                result = getPort()
                lastScan = now
                if (result == None): 
                    continue
                p = setupPort(result)
                detectPort = False
            
            while not detectPort:
                gotPackage = p.dispatch(1, sniff.detectPrintMessage)
                if (gotPackage == 0):
                    result = getPort()
                    if (result == None):
                        detectPort = True

    except KeyboardInterrupt:
        print '%s' % sys.exc_type
        print 'shutting down'
        print '%d packets received, %d packets dropped, %d packets dropped by interface' % p.stats()

if __name__ == '__main__':
    main()

import psutil
import pcap
import sniff
import sys

executableName = "dota_linux"

def getPort():
    for p in psutil.process_iter():
        if (p.name() == executableName):
            for c in p.connections():
                if c.status == 'NONE': # Status NONE is _obviously_ the one :S
                    return c.laddr[1]  # laddr = (ip-address, port)

# Taken from sniff.py in pylibpcap
def main():
    result = getPort()
    if (result == None): return
    p = pcap.pcapObject()
    dev = "eth0"
    net, mask = pcap.lookupnet(dev)
    p.open_live(dev, 1600, 0, 100)
    filterString = "port " + str(result)
    p.setfilter(filterString, 0, 0)

    try:
        while 1:
            p.dispatch(1, sniff.detectPrintMessage)
    except KeyboardInterrupt:
        print '%s' % sys.exc_type
        print 'shutting down'
        print '%d packets received, %d packets dropped, %d packets dropped by interface' % p.stats()

if __name__ == '__main__':
    main()

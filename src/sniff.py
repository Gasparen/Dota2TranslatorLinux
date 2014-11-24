import pcap
import socket
import struct
import translate

ALL_CHAT_IDENTIFIER = "DOTA_Chat_All"
TEAM_CHAT_IDENTIFIER = "DOTA_Chat_Team"

# Taken from sniff.py in pylibpcap
def decode_ip_packet(s):
    d={}
    d['version']=(ord(s[0]) & 0xf0) >> 4
    d['header_len']=ord(s[0]) & 0x0f
    d['tos']=ord(s[1])
    d['total_len']=socket.ntohs(struct.unpack('H',s[2:4])[0])
    d['id']=socket.ntohs(struct.unpack('H',s[4:6])[0])
    d['flags']=(ord(s[6]) & 0xe0) >> 5
    d['fragment_offset']=socket.ntohs(struct.unpack('H',s[6:8])[0] & 0x1f)
    d['ttl']=ord(s[8])
    d['protocol']=ord(s[9])
    d['checksum']=socket.ntohs(struct.unpack('H',s[10:12])[0])
    d['source_address']=pcap.ntoa(struct.unpack('i',s[12:16])[0])
    d['destination_address']=pcap.ntoa(struct.unpack('i',s[16:20])[0])
    if d['header_len']>5:
        d['options']=s[20:4*(d['header_len']-5)]
    else:
        d['options']=None
    d['data']=s[4*d['header_len']:]
    return d


def detectPrintMessage(pktlen, data, timestamp):
    if not data:
        return

    if data[12:14]=='\x08\x00':
        decoded = decode_ip_packet(data[14:])
        data = decoded['data']

    identifierLength = len(ALL_CHAT_IDENTIFIER) + 2
    chatFound = str.find(data, ALL_CHAT_IDENTIFIER)
    type = 0
    
    if (chatFound == -1):
        identifierLength = len(TEAM_CHAT_IDENTIFIER) + 2
        chatFound = str.find(data, TEAM_CHAT_IDENTIFIER)
        type = 1

    if (chatFound != -1):
        indexName = chatFound + identifierLength
        lengthName = ord(data[indexName - 1]) # Get the ascii-value
        indexMessage = indexName + lengthName + 2
        lengthMessage = ord(data[indexMessage - 1]) # Get the ascii-value
        
        name = data[indexName:indexName+lengthName]
        message = data[indexMessage:indexMessage+lengthMessage]
        
        print "[Allies] " if (type==1) else "", name, ": ", message, " => ", translate.translate(message)

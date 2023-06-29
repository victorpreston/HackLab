#!/usr/bin/env python2
import socket;
import os;
import struct;
from ctypes import *;
import threading as thread;
import time;
from netaddr import IPNetwork, IPAddress;

# Define the IP and subnet
host   = "192.168.0.1";
subnet = "192.168.0.0/24";
magic  = "SOME_FRIES_MOTHERFUCKER";

def udpSender(subnet, magic):
    time.sleep(5);
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic, ("%s" % ip,65212));
        except:
            pass;

class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte, 8),
        ("len", c_ushort, 16),
        ("id", c_ushort, 16),
        ("offset", c_ushort, 16),
        ("ttl", c_ubyte, 8),
        ("protocol_num", c_ubyte, 8),
        ("sum", c_ushort, 16),
        ("src", c_uint, 32),
        ("dst", c_uint, 32)
    ];

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer);

    def __init__(self, socket_buffer=None):
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"};
        self.src_address  = socket.inet_ntoa(struct.pack("<L", self.src));
        self.dst_address  = socket.inet_ntoa(struct.pack("<L", self.dst));

        try:
            self.protocol = self.protocol_map[self.protocol_num];
        except:
            self.protocol = str(self.protocol_num);

class ICMP(Structure):
    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort)
    ];

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer);

    def __init__(self, socket_buffer):
        pass;

if os.name == "nt":
    protocol = socket.IPPROTO_IP;
else:
    protocol = socket.IPPROTO_ICMP;

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, protocol);
sniffer.bind((host, 0));
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1); # IP Header

if os.name == "nt": # Promiscuous mode (windows)
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON);

t = thread.Thread(target=udpSender, args=(subnet, magic));
t.start();

try:
    while True:
        raw_buffer = sniffer.recvfrom(65565)[0];
        ip_header  = IP(raw_buffer[0:20]);
        #print "Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address);

        if ip_header.protocol == "ICMP":
            offset      = ip_header.ihl * 4;
            buff        = raw_buffer[offset:offset + sizeof(ICMP)];
            icmp_header = ICMP(buff);
            #print "ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code);
            if icmp_header.code == 3 and icmp_header.type == 3:
                if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                    if raw_buffer[len(raw_buffer) - len(magic):] == magic:
                        print "Host Found: %s" % ip_header.src_address;

# Handle CTRL-C
except KeyboardInterrupt:
    if os.name == "nt": # Turn off promiscuous
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF); 

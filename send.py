#!/usr/bin/env python

import socket

MCAST_GRP = '224.0.0.1'
MCAST_PORT = 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
sock.sendto(bytes("Hello World", "utf-8"), (MCAST_GRP, MCAST_PORT))

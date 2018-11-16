#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:     raw_http.py
# Purpose:       construct a raw http get packet
#
# Author:    Yangjun
#
# Created:       08/02/2014
# Copyright:   (c) Yangjun 2014
# Licence:       <your licence>
# -------------------------------------------------------------------------------

import sys
import socket
from impacket import ImpactPacket


def main():
    #if len(sys.argv) < 3:
    #    print
    #    "Use: %s <src ip> <dst ip>" % sys.argv[0]
    #    print
    #    "Use: %s <src ip> <dst ip> <cnt>" % sys.argv[0]
    #    sys.exit(1)
    #elif len(sys.argv) == 3:
    #    #源IP
    #    src = sys.argv[1]
    #    #目标IP
    #    dst = sys.argv[2]
    #    #发送次数
    #    cnt = 1
    #elif len(sys.argv) == 4:
    #    #源IP
    #    src = sys.argv[1]
    #    #目标IP
    #    dst = sys.argv[2]
    #    #发送次数
    #    cnt = sys.argv[3]
    #else:
    #    print
    #    "Input error!"
    #    sys.exit(1)

    src="127.0.0.1"
    dst="127.0.0.1"
    cnt=10
    # print src, dst
    ip = ImpactPacket.IP()
    ip.set_ip_src(src)
    ip.set_ip_dst(dst)

    # Create a new ICMP packet of type ECHO.
    icmp = ImpactPacket.ICMP()

    tcp = ImpactPacket.TCP()
    tcp.set_th_sport(8081)
    tcp.set_th_dport(8009)
    tcp.set_th_seq(1)
    tcp.set_th_ack(1)
    tcp.set_th_flags(0x18)
    tcp.set_th_win(64)

    tcp.contains(ImpactPacket.Data(
        "GET /att/DIYLife/41264/528 HTTP/1.1\r\nHost: 172.16.11.4\r\nAccept-Encoding: identity\r\n\r\n"))

    ip.contains(tcp)

    # Open a raw socket. Special permissions are usually required.
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    seq_id = 0
    while cnt >= 1:
        # Calculate its checksum.
        seq_id = seq_id + 1
        tcp.set_th_seq(seq_id)
        tcp.calculate_checksum()

        # Send it to the target host.
        s.sendto(ip.get_packet(), (dst, 8007))
        cnt = cnt - 1
        print("已发送：源IP：{}，".format(ip.get_ip_src()))
        print("目标IP{}\n".format(ip.set_ip_dst()))


if __name__ == '__main__':
    main()
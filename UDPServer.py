# -*- coding:utf-8 -*-

"""
 UDP 服务器
"""

import socket
import Packet

G_Packet = Packet.Packet()


def SocketHandler(sock):
    """
    协程处理
    :param sock:
    :return:
    """
    total_packet = 0
    while True:
        data, address = sock.recvfrom(8192)
        G_Packet.writeMulitBytes(data)
        G_Packet.position = 0
        while G_Packet.length() > 4:
            pack_size = G_Packet.readShort()
            if pack_size > G_Packet.length() - 2:
                G_Packet.position = G_Packet.length()
                break
            else:
                data = G_Packet.readMulitBytes(pack_size)
                total_packet += 1
                h_size = G_Packet.length() - G_Packet.position
                if h_size == 0:
                    G_Packet.clear()
                else:
                    G_Packet.reset(G_Packet.readMulitBytes(h_size))
        sock.sendto(data, address)
        # if total_packet % 10000 == 0:
        #     print("RecvPack::: {0}", total_packet)

def run_main_udp():
    """
    运行
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
    sock.bind(("0.0.0.0", 8088))
    handler = SocketHandler(sock)


if __name__ == "__main__":
    run_main_udp()
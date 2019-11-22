# -*- coding:utf-8 -*-

"""
 TCP 服务器
"""

import socket
import Packet
import selectors

G_Packet = Packet.Packet()


def SocketHandler():
    """
    协程处理
    :param sock:
    :return:
    """
    total_packet = 0

    while True:
        sock = yield
        try:
            data = sock.recv(8192)
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
            sock.sendall(data)
            # if total_packet % 10000 == 0:
            #     print("RecvPack::: {0}", total_packet)
        except:
            pass



def run_main_udp():
    """
    运行
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
    sock.bind(("0.0.0.0", 8088))
    sock.listen(1000)
    sock.setblocking(False)
    handler = SocketHandler()
    handler.send(None)
    selector = selectors.DefaultSelector()
    selector.register(sock, selectors.EVENT_READ)
    while True:
        ready = selector.select()
        for key, mask in ready:
            if key.fileobj == sock:
                client, address = sock.accept()
                client.setblocking(False)
                selector.register(client, selectors.EVENT_READ)
            else:
                handler.send(key.fileobj)


if __name__ == "__main__":
    run_main_udp()
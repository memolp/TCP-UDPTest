# -*- coding:utf-8 -*-

"""
 TCP 客户端
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

import time
def send(sock):
    for i in range(1000):
        # 发送的数据需要再重新包装
        sendPacket = Packet.Packet()
        # 起始标记
        sendPacket.writeUnsignedByte(0xEF)
        # 协议长度-预先站位
        sendPacket.writeUnsignedInt(0)
        # 用户vuer
        sendPacket.writeUnsignedInt(1)
        # 发送的序列号
        sendPacket.writeInt64(int(time.time() * 1000))
        # sockid
        sendPacket.writeUnsignedByte(1)
        # 消息ID
        sendPacket.writeUnsignedShort(2000)
        # 内容
        sendPacket.writeUTFBytes("asdasdkkkkk99sd0fsd909sdf9sd0fs90df09sd90fsd09fsd90f09")
        # 更新长度
        sendPacket.position = 1
        # 写入正确的协议长度 不包含起始标记和长度自己
        sendPacket.writeUnsignedInt(sendPacket.length() - 5)
        # 发送数据
        buff = sendPacket.getvalue()

        sock.sendall(buff)
    #time.sleep(2)

def run_main_udp():
    """
    运行
    :return:
    """

    import binascii
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    sock.connect(("127.0.0.1",7090))
    for i in range(1000):
        send(sock)
        time.sleep(1)
    #print(binascii.hexlify(buff))



if __name__ == "__main__":
    run_main_udp()
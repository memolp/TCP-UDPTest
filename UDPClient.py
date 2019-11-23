# -*- coding:utf-8 -*-

"""
  UDP客户端
"""


import socket
import Packet
import threading

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
        total_packet += 1
        # G_Packet.writeMulitBytes(data)
        # G_Packet.position = 0
        # while G_Packet.length() > 4:
        #     pack_size = G_Packet.readShort()
        #     if pack_size > G_Packet.length() - 2:
        #         G_Packet.position = G_Packet.length()
        #         break
        #     else:
        #         data = G_Packet.readMulitBytes(pack_size)
        #         total_packet += 1
        #         h_size = G_Packet.length() - G_Packet.position
        #         if h_size == 0:
        #             G_Packet.clear()
        #         else:
        #             G_Packet.reset(G_Packet.readMulitBytes(h_size))
        # sock.sendto(data, address)
        # if total_packet % 10000 == 0:
        #     print("RecvPack::: {0}", total_packet)
        #print("total_packet:",total_packet)

import time
def CreatePacket():
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
    return buff

def run_main_udp():
    """
    运行
    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 102400000)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024000)
    sock.connect(("127.0.0.1",7090))
    buff = CreatePacket()
    p = threading.Thread(target=SocketHandler, args=(sock,))
    p.start()
    for i in range(100):
        start = time.time() * 1000
        for i in range(30000):
            sock.sendto(buff, ("127.0.0.1", 7090))
        cost = time.time() * 1000 - start
        if cost < 1000:
            time.sleep( (1000 - cost ) / 1000)
        else:
            print("cost::::", cost)
    time.sleep(3)

if __name__ == "__main__":
    run_main_udp()

from socket import *


def client():
    # 创建socket
    tcp_client_socket = socket(AF_INET, SOCK_STREAM)

    # 服务器的地址
    # '192.168.43.1'表示目的ip地址
    # 8080表示目的端口
    dest_addr = ('127.0.0.1', 7788)  # 注意 是元组，ip是字符串，端口是数字

    # 链接服务器，进行tcp三次握手
    tcp_client_socket.connect(dest_addr)

    while True:
        # 从键盘获取数据
        send_data = input("请输入要发送的数据:")

        # 判断输入stop，则退出客户端
        if send_data == "stop":
            break

        # 发送数据到指定的服务端
        tcp_client_socket.send(send_data.encode("utf-8"))

        # 接收对方发送过来的数据，最大接收1024个字节
        recvData = tcp_client_socket.recv(1024)
        print('接收到的数据为:', recvData.decode('utf-8'))

    # 关闭套接字
    tcp_client_socket.close()


if __name__ == '__main__':
    client()


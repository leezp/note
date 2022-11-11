from socket import *


def server():
    # 创建套接字
    tcp_server_socket = socket(AF_INET, SOCK_STREAM)

    # 绑定服务端提供服务的端口号
    local_addr = ('', 7788)  # ip地址和端口号，ip一般不用写，表示本机的任何一个ip

    # 绑定
    tcp_server_socket.bind(local_addr)

    # 使用socket创建的套接字默认的属性是主动的，使用listen将其改为被动，用来监听连接
    tcp_server_socket.listen(128)

    # 如果有新的客户端来链接服务端，那么就产生一个新的套接字专门为这个客户端服务
    # client_socket用来为这个客户端服务
    # tcp_server_socket就可以省下来专门等待其他新的客户端连接while True:
    client_socket, clientAddr = tcp_server_socket.accept()

    while True:

        # 接收对方发送的数据
        recv_data = client_socket.recv(1024)  # 1024表示本次接收的最大字节数
        print('接收到客户端的数据为:', recv_data.decode('utf-8'))

        # 将客户端的数据，转发至另一个服务器
        # 创建新的tcp连接，连接上另一个服务器
        proxy_tcp_conn = socket(AF_INET, SOCK_STREAM)
        proxy_tcp_conn.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 建立新的 TCP 端口
        proxy_tcp_conn.connect(('10.88.104.26', 8080))  # 连接 TCP ServerB 服务 使用 NetAssist.exe 模拟
        proxy_tcp_conn.send(recv_data)  # 将接收到的数据发向另一个服务器
        proxy_recv_msg = proxy_tcp_conn.recv(1024)  # 接收TCP ServerB 服务返回的数据
        print("接收到另一个服务的信息: " + proxy_recv_msg.decode())

        # 发送一些数据到客户端
        client_socket.send(proxy_recv_msg)

        # 将接收到的数据转换为字符串打印
        recv_result = str(recv_data.decode('utf-8'))
        # print("recv_result", recv_result)

        # 当接收到stop，则停止服务
        if recv_result == "stop":
            break

    # 关闭为这个客户端服务的套接字，只要关闭，就意味着不能再为这个客户端服务了。
    # 如果客户端还需要服务，则重新建立连接
    client_socket.close()

    ## 最后关闭监听的socket
    tcp_server_socket.close()


if __name__ == '__main__':
    server()

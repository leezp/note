# -*- coding:utf-8 -*-
import socketserver

client_list = []


class TCPHandler(socketserver.BaseRequestHandler):
    # 所有请求的交互都是在handle里执行的,
    def handle(self):
        while True:
            try:
                # 每一个请求都会实例化TCPHandler(socketserver.BaseRequestHandler):
                self.data = self.request.recv(80000).strip()
                client_ip = self.client_address[0]
                client_num = self.client_address[1]
                if client_num not in client_list:
                    client_list.append(client_num)
                print("来访客户端IP:{} 编号：{}".format(client_ip, client_num))
                # print("客户端数据：",self.data.decode())
                # 发送回客户端的数据
                self.request.sendall(self.data)  # 也可自定以返回内容
                break
                # print("-------当前在线客户端编号列表-----------")
                # print(client_list)
            except ConnectionResetError as e:
                print("----断开的客户端------")
                print("客户端：{} 已经断开".format(client_num))
                # 如果有客户端掉线，则将它从在线列表中删除
                client_list.remove(client_num)
                break


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8080
    server = socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler)  # 线程
    server.serve_forever()

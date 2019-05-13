from socket import *

BUFSIZE = 1024
HOST = ''
PORT = 10000
ADDR = (HOST, PORT)


class FoodServer():
    server_socket = []
    client_socket = []


    def __init__(self):
        pass

    def create_connector(self):
        pass


class FoodServerConnector:
    server_socket = 0
    client_socket = 0
    addr_info = 0

    def run(self):
        # 소켓 생성
        self.server_socket = socket(AF_INET, SOCK_STREAM)

        # 소켓 주소 정보 할당
        self.server_socket.bind(ADDR)
        print('[Now] : bind')

        # 연결 수신 대기 상태
        self.server_socket.listen(100)
        while True:
            # 연결 수락
            self.client_socket, self.addr_info = self.server_socket.accept()
            print('[Now] : accept')
            print('--client information--')
            print(self.client_socket)


class FoodServerReceiver:
    server_socket = 0
    client_socket = 0

    def __init__(self, server_socket, client_socket):
        self.server_socket = server_socket
        self.client_socket = client_socket

    def run(self):
        while True:
            data = self.client_socket.recv(BUFSIZE)
            print('[RECV] : ', data.decode())


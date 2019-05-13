from socket import *

BUFSIZE = 1024
HOST = ''
PORT = 10000
ADDR = (HOST, PORT)


class FoodServer():
    list_server_socket = []
    list_client_socket = []


    def __init__(self):
        pass

    def create_connector(self):
        pass


class FoodServerConnector:
    list_server_socket = []
    list_client_socket = []
    addr_info = 0

    def __init__(self, server_socket, client_socket):
        self.list_server_socket = server_socket
        self.list_client_socket = client_socket

    def run(self):
        # 소켓 생성
        _server_socket = socket(AF_INET, SOCK_STREAM)

        # 소켓 주소 정보 할당
        _server_socket.bind(ADDR)
        print('[Now] : bind')

        # 연결 수신 대기 상태
        _server_socket.listen(100)
        while True:
            # 연결 수락
            _client_socket, self.addr_info = _server_socket.accept()
            self.list_server_socket.append(_server_socket)
            self.list_client_socket.append(_client_socket)
            print('[Now] : accept')
            print('--client information--')
            print(_client_socket)


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


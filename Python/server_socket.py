from socket import *
import threading

BUFSIZE = 1024
HOST = ''
PORT = 10000
ADDR = (HOST, PORT)


class FoodServer:
    list_server_socket = []
    list_client_socket = []
    list_client_receiver = []
    client_connector = 0

    def __init__(self):
        pass

    def get_list_client_socket(self):
        return self.list_client_socket

    def create_connector(self):
        self.client_connector = FoodServerConnector(self.list_client_socket, self.list_client_receiver)
        self.client_connector.start()

    def exit_server(self):
        for client_socket in self.list_client_receiver:
            client_socket.exit_receiver()
        print('[NOW] : Receiver Exit')
        self.client_connector.exit_connector()
        print('[NOW] : Connector Exit')


class FoodServerConnector(threading.Thread):
    list_client_socket = []
    list_client_receiver = []
    _server_socket = 0
    addr_info = 0
    flag = 1

    def __init__(self, client_socket, client_receiver):
        threading.Thread.__init__(self)
        self.list_client_socket = client_socket
        self.list_client_receiver = client_receiver

    def get_list_client_socket(self):
        return self.list_client_socket

    def exit_connector(self):
        self.flag = 0

    def run(self):
        # 소켓 생성
        _server_socket = socket(AF_INET, SOCK_STREAM)

        # 소켓 주소 정보 할당
        _server_socket.bind(ADDR)
        print('[Now] : Bind')

        # 연결 수신 대기 상태(인자 값은 몇 명까지 접속을 허용할 것인지 뜻함)
        _server_socket.listen(100)
        while self.flag:
            # 연결 수락
            _client_socket, self.addr_info = _server_socket.accept()
            self.list_client_socket.append(_client_socket)
            print('[Now] : Accept')
            print('--client information--')
            print(_client_socket)
            socket_receiver = FoodServerReceiver(_client_socket)
            self.list_client_receiver.append(socket_receiver)
            socket_receiver.start()
            print('[Now] : Receiver Start')


class FoodServerReceiver(threading.Thread):
    client_socket = 0
    flag = 1

    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket

    def exit_receiver(self):
        self.flag = 0

    def run(self):
        while self.flag:
            print('[Now] : Waiting Msg')
            data = self.client_socket.recv(BUFSIZE)
            print('[RECV] : ', data.decode())


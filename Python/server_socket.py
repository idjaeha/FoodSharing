from socket import *
from random import *
import threading, csv
import server_db
from datetime import datetime, timedelta

BUFSIZE = 1024
HOST = ''
PORT = 10000
ADDR = (HOST, PORT)


class FoodServer:
    """
    소켓과 DB를 관리하고 각종 기능들을 수행하는 클래스
    """
    list_server_socket = []
    list_client_socket = []
    list_client_receiver = []
    client_connector = 0
    food_server_db = 0

    def __init__(self):
        self.food_server_db = server_db.FoodServerDB()

    def get_list_client_socket(self):
        """
        클라이언트 소켓 정보를 리스트로 반환합니다.
        """
        return self.list_client_socket

    def create_connector(self):
        """
        소켓 서버의 커넥터를 생성합니다.
        """
        self.client_connector = FoodServerConnector(self.list_client_socket, self.list_client_receiver)
        self.client_connector.start()

    def exit_server(self):
        """
        서버를 종료합니다.
        """
        for client_socket in self.list_client_receiver:
            client_socket.exit_receiver()
        print('[NOW] : Receiver Exit')
        self.client_connector.exit_connector()
        print('[NOW] : Connector Exit')

    def create_csv_row(self, data, filename="output.csv", file_location="./"):
        """
        list 형태로 받은 data를 csv 파일 형태로 만들어냅니다.
        data는 리스트들로 이루어져있으며 리스트의 첫번째 값은 각 행의 제목을 뜻합니다.
        filename을 인자 값으로 주지 않는다면 output.csv 을 제목으로 사용합니다.
        """
        fieldnames = []
        # 제목을 fieldnames에 저장합니다.
        for i in data[0]:
            fieldnames.append(i)
        file_name = file_location + filename
        f = open(file_name, 'w', encoding='euc-kr', newline='')
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        for idx_i in range(1, len(data)):
            writer.writerow(data[idx_i])

    def create_search_data(self, num=500):
        """
        랜덤으로 유저의 검색 기록을 만들어주는 함수
        :param num
        :return:
        """
        test_search = []

        example = \
            [["한식", "비빔밥", "불고기", "된장찌개", "김치찌개", "김치전", "떡갈비"],
             ["중식", "자장면", "짬뽕", "탕수육", "깐풍기", "팔보채", "칠리새우"],
             ["양식", "파스타", "스테이크", "샐러드", "오믈렛", "햄버거", "피자"],
             ["일식", "초밥", "가츠동", "우동", "텐동", "라멘", "사시미"],
             ["분식", "떡볶이", "김밥", "튀김", "순대", "오뎅", "주먹밥"]]

        temp_times = []
        # 랜덤으로 시간을 생성
        for i in range(num):
            start = datetime.now()
            end = start + timedelta(days=7)
            temp_times.append(start + (end - start) * random())
        temp_times.sort()

        for i in range(num):
            temp = []
            temp.append(i + 1)
            temp.append(randint(1, 6))
            temp.append(temp_times[i])
            temp.append(randint(1,60))
            test_search.append(temp)

        return test_search

    def create_food_data(self):
        """
        랜덤으로 음식 데이터를 만들어주는 함수
        :param csv_flag:
        :return:
        """
        test_food = []
        example = \
            [["한식", "비빔밥", "불고기", "된장찌개", "김치찌개", "김치전", "떡갈비"],
             ["중식", "자장면", "짬뽕", "탕수육", "깐풍기", "팔보채", "칠리새우"],
             ["양식", "파스타", "스테이크", "샐러드", "오믈렛", "햄버거", "피자"],
             ["일식", "초밥", "가츠동", "우동", "텐동", "라멘", "사시미"],
             ["분식", "떡볶이", "김밥", "튀김", "순대", "오뎅", "주먹밥"]]
        flag = 0
        food_num = 1
        rest_num = 0
        temp_food_list = []

        while rest_num < 20:
            temp = []
            temp.append(food_num)
            temp.append(rest_num + 1)
            temp.append(example[rest_num % 5][0])
            temp_food = example[rest_num % 5][randint(1, 6)]
            if temp_food not in temp_food_list:
                temp.append(temp_food)
                temp_food_list.append(temp_food)
            else:
                continue

            food_num += 1
            flag += 1
            test_food.append(temp)

            if flag > 2:
                flag = 0
                rest_num += 1
                temp_food_list = []

        return test_food

    def create_user_data(self, csv_flag=False):
        """
        랜덤으로 유저 데이터를 만들어주는 함수
        :param csv_flag:
        :return:
        """
        test_user = []
        user_name = ["철수", "영희", "재하", "예은", "지호", "민호"]
        user_num = 1

        for i in range(6):
            temp = []
            temp.append(user_num)
            temp.append(user_name[i])
            temp.append("1234")
            for i in range(5):
                temp.append(-1)
            test_user.append(temp)
            user_num += 1

        return test_user
    
    def create_rest_data(self, csv_flag=False):
        """
        랜덤으로 가게 데이터를 만들어주는 함수
        :param csv_flag:
        :return:
        """
        test_rest = []
        user_name = ["재하", "지호", "민호", "예은"]
        category = ["한식", "중식", "양식", "일식", "분식"]
        sample_name = [["구백집", "전주식당", "정성찬", "윤씨네", "큰뫼"],
                       ["하리원", "승리장", "중국집", "중화마루", "향만옥"],
                       ["리틀 파스타", "피터팬 스테이크", "서양집", "몽마르 언덕", "서가앤쿡"],
                       ["스시현", "스시마루", "홍연집", "스타동", "텐동"],
                       ["윤가네", "김밥천국", "한성 분식", "신전떡볶이", "미스터 돈까스", "라면 일번지"]]
        rest_num = 1

        for name in user_name:
            for i in range(5):
                temp = []
                temp.append(rest_num)
                temp.append(name + "의 " + sample_name[i][randrange(len(sample_name[i]))])
                temp.append(category[i])
                temp.append(randint(-500, 500))
                temp.append(randint(-500, 500))
                test_rest.append(temp)
                rest_num += 1

        if csv_flag:
            test_rest.insert(0, ["rest_num", "rest_name", "category", "x", "y"])
            self.create_csv_row(test_rest, "rest_data.csv")
        return test_rest

    def create_person_csv(self, user_num):
        title = ["Search_Category", "Search_Time", "Search_Word"]
        result = self.food_server_db.select_human_csv(user_num)
        result.insert(0, title)
        self.create_csv_row(result, "person{0}.csv".format(user_num), "./data/person/")

    def add_search_data(self, user_num, food_num):
        """
        search 테이블에 값을 추가하는 함수
        :param user_num:
        :param food_num:
        :return:
        """
        num = self.food_server_db.get_data_num("search") + 1
        search_value = [num, user_num, datetime.now(), food_num]

        self.food_server_db.insert_search_data(search_value)

    def create_basic_table(self):
        self.food_server_db.create_table()


class FoodServerConnector(threading.Thread):
    """
    클라이언트와의 연결을 위해 대기하는 커넥터
    """
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
    """
    클라이언트들의 메세지를 받기 위해 대기하는 리시버
    """
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


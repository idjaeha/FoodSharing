#-*- coding: euc-kr -*-

from socket import *
from random import *
import threading, csv
import server_db
from datetime import datetime, timedelta
import glob
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split

BUFSIZE = 512
HOST = ''
PORT = 3000
ADDR = (HOST, PORT)
room_info = {}

class FoodServer:
    """
    소켓과 DB를 관리하고 각종 기능들을 수행하는 클래스
    """
    list_server_socket = []
    list_client_socket = []
    list_client_receiver = []
    client_connector = 0
    food_server_db = 0
    top5_list = [[]]
    user_top5_list = [[]]

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
            temp.append(i)
            temp.append(randint(0, 5))
            temp.append(temp_times[i])
            temp.append(randint(1, 60))
            test_search.append(temp)

        return test_search

    def insert_search_data(self, category = None, user_num = None, num=500):
        """
        랜덤으로 유저의 검색 기록을 추가해주는 함수
        :param num
        :return:
        """
        test_search = []
        start_num = self.food_server_db.get_data_num("search")

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
            temp.append(start_num + i + 1)
            temp.append(str(user_num))
            temp.append(temp_times[i])
            if category == "한식":
                temp.append(str(randint(1, 3)))
            elif category == "중식":
                temp.append(str(randint(4, 6)))
            elif category == "양식":
                temp.append(str(randint(7, 9)))
            elif category == "일식":
                temp.append(str(randint(10, 12)))
            elif category == "분식":
                temp.append(str(randint(13, 15)))
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
        user_name = ["0", "1", "2", "3", "4", "5"]
        user_num = 0

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
        title = ["Search_Category", "Search_Time", "Search_Word", "id"]
        result = list(self.food_server_db.select_human_csv(user_num))
        result1 = []

        for data in result:
            temp = list(data)
            temp.append(user_num)
            result1.append(temp)
        result1.insert(0, title)
        self.create_csv_row(result1, "person{0}.csv".format(user_num), "./data/person/")

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

    def food_analysis(self, input_id_int, top5_list, user_ac_list):
        input_path = "./data/person/"
        rows_num = 80

        # 현재 시간 전부
        currentTime = datetime.now()
        # 7일전
        currentTime7 = currentTime - timedelta(days=7)

        # 현재 시간만
        ct = currentTime.hour

        allFiles = glob.glob(input_path + "*.csv")
        people = len(allFiles)
        allData = pd.DataFrame()
        list_ = []
        classification_ = []
        allClassification_df = []

        # 모든 파일 데이터 통합
        for file_ in allFiles:
            df = pd.read_csv(file_, index_col=None, header=0, encoding="euc-kr")
            Classification_df = df[['Search_Time', 'Search_Word']]
            list_.append(df)
            classification_.append(Classification_df)

        # BestSeller 시작
        allClassification_df = pd.concat(classification_)
        allData = pd.concat(list_)

        # 7일 이상된 row 제거
        allData['Search_Time'] = pd.to_datetime(allData['Search_Time'])

        # 시간 분류
        Time = []
        temp_Menu = allData.Search_Word
        Menu = temp_Menu.values.tolist()
        df_list = allClassification_df.values.tolist()

        for item in df_list:
            for t in range(1):
                temp_t = str(item[t])
                temp_Day = temp_t[5:7]
                temp_Time = int(temp_t[11:13])
                Time.append(temp_Time)

        # 메뉴와 시간만 받는 데이터생성
        data = pd.DataFrame({'Time': Time,
                             'Menu': Menu})

        # 각각의 시간과 날짜 별로 list 생성
        timeDic = {}
        timeDic['Morning'] = data.loc[(10 >= data["Time"]) & (data["Time"] > 6), :]
        timeDic['Lunch'] = data.loc[(10 >= data["Time"]) & (data["Time"] > 6), :]
        timeDic['Dinner'] = data.loc[(10 >= data["Time"]) & (data["Time"] > 6), :]
        Midnight1 = data.loc[(24 >= data["Time"]) & (data["Time"] > 20), :]
        Midnight2 = data.loc[(6 >= data["Time"]) & (data["Time"] >= 0), :]
        Midnight = Midnight1.append(Midnight2)
        timeDic['Midnight'] = Midnight1.append(Midnight2)

        def printTimeTop5(ct, time):
            # one hot encoding
            time_df = pd.get_dummies(timeDic[time].Menu)

            sum_time_df = pd.DataFrame(time_df.sum(axis=0), columns=["count"])
            sort_time_df = sum_time_df.sort_values(by="count", ascending=False)
            top_time_df = sort_time_df[0:5].index.tolist()

            return list(top_time_df)

        # 시간별로 다루는 list 종류
        if ct >= 10 and 6 > ct:
            temp = printTimeTop5(ct, 'Morning')
        elif 16 >= ct and ct > 10:
            temp = printTimeTop5(ct, 'Lunch')
        elif 20 >= ct and ct > 16:
            temp = printTimeTop5(ct, 'Dinner')
        else:
            temp = printTimeTop5(ct, 'Midnight')

        top5_list[0] = temp

        def addPersonData(top5List, count):
            personList = []
            for i in range(count):
                # 사람0의 데이터 분석
                person_df = allData.loc[allData["id"] == i]
                person_search_df = person_df[["Search_Category", "Search_Word"]]
                person_onehot_search_word_data = pd.get_dummies(person_search_df.Search_Word)

                # 사람0의 탑5 메뉴
                sum_person_df = pd.DataFrame(person_onehot_search_word_data.sum(axis=0), columns=["count"])
                sort_sum_person_df = sum_person_df.sort_values(by="count", ascending=False)
                top5_person_df = sort_sum_person_df[0:5].index.tolist()

                person_data = person_onehot_search_word_data
                person_label = person_df[["Search_Category"]]

                # 학습 전용 데이터와 테스트 전용 데이터로 나누기
                person_data_train, person_data_test, person_label_train, person_label_test = train_test_split(
                    person_data,
                    person_label,
                    test_size=rows_num)
                personList.append(person_label_test)
                top5List.append(top5_person_df)

            return personList

        personTop5Datas = []
        personDatas = addPersonData(personTop5Datas, people)

        # 학습, 예측

        # 사람별 취향 일치율
        ac_scores = []
        for i in range(len(personDatas)):
            scoreList = []
            for j in range((len(personDatas) - 1) - i):
                scoreList.append(metrics.accuracy_score(personDatas[i], personDatas[j + 1 + i]))
            if len(scoreList) != 0:
                ac_scores.append(scoreList)

        # 취향에 따른 추천
        id_ac_list = []
        for i in range(input_id_int):
            id_ac_list.append(ac_scores[i][input_id_int - 1 - i])

        if input_id_int < len(ac_scores):
            for i in range(len(ac_scores[input_id_int])):
                id_ac_list.append(ac_scores[input_id_int][i])

        id_ac_list.insert(input_id_int, -1)
        max_idx = id_ac_list.index(max(id_ac_list))
        user_ac_list[0] = personTop5Datas[max_idx]
        #print(ac_scores)

    def update_user_top5(self, user_num, flag=True):
        """
        실시간 검색 top5_list와 인자로 받은 유저 취향에 맞춘 top5를 얻을 수 있는 메서드
        flag를 False로 하게 되면 해당 정보가 db에는 넘어가지 않는다.
        :param user_num: 
        :param flag: 
        :return: 
        """
        self.food_analysis(int(user_num), self.top5_list, self.user_top5_list)
        if flag:
            self.food_server_db.update_user_top5(user_num, self.user_top5_list[0])


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
            socket_receiver = FoodServerReceiver(_client_socket, self.list_client_socket)
            self.list_client_receiver.append(socket_receiver)
            socket_receiver.start()
            print('[Now] : Receiver Start')


class FoodServerReceiver(threading.Thread):
    """
    클라이언트들의 메세지를 받기 위해 대기하는 리시버
    """
    client_socket = 0
    flag = 1
    list_client_socket = []
    food_server_db = 0
    food_server = 0

    def __init__(self, client_socket, list_client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.list_client_socket = list_client_socket
        self.food_server_db = server_db.FoodServerDB()
        self.food_server = FoodServer()

    def exit_receiver(self):
        self.flag = 0

    def run(self):
        while self.flag:
            try:
                print('[Now] : Waiting Msg')
                data = self.client_socket.recv(BUFSIZE)
                msg = data.decode("euc-kr")
                print('[Recv] : ', msg)
                self.process_recv_msg(msg)
            except:
                print("[Close] : ", self.client_socket)
                self.list_client_socket.remove(self.client_socket)
                break

    def process_recv_msg(self, msg):
        msg_list = msg.split("//")
        cmd = msg_list[0]
        print("[Cmd] : " + cmd)
        if cmd == "0":
            # 서버 연결 응답
            self.send_msg("0//")
        elif cmd == "1":
            # 로그인 성공, 실패
            id = msg_list[1]
            pwd = msg_list[2]
            rows = self.food_server_db.get_user_using_info(id, pwd)
            print(rows)
            if len(rows) == 1:
                user_num = str(rows[0][0])
                print(user_num)
                self.food_server.update_user_top5(user_num)
                #print(self.food_server.top5_list)
                msg = "2//1//" + user_num + "//" + "//".join(rows[0][1:]) + "//"
                print(msg)
            else:
                msg = "2//0//"
            self.send_msg(msg)
        elif cmd == "3":
            # top5 리스트 응답
            self.food_server.update_user_top5(0, False)
            top5_msg = "4//" + "//".join(self.food_server.top5_list[0]) + "//"
            self.send_msg(top5_msg)
        elif cmd == "5":
            # 식당 자료 요청
            if msg_list[1] == "0":
                category = msg_list[2]
                rest = self.food_server_db.select_rest_data(category)
                num = len(rest)
                msg = "6//0//{0}//".format(num)
                for i in range(num):
                    rest[i] = list(rest[i])
                    for j in range(len(rest[i])):
                        rest[i][j] = str(rest[i][j])
                    msg = msg + "//".join(rest[i]) + "//"
            elif msg_list[1] == "1":
                food = msg_list[2]
                rest = self.food_server_db.select_rest_data(food, True)
                num = len(rest)
                msg = "6//1//{0}//".format(num)
                for i in range(num):
                    rest[i] = list(rest[i])
                    for j in range(len(rest[i])):
                        rest[i][j] = str(rest[i][j])
                    msg = msg + "//".join(rest[i]) + "//"
            self.send_msg(msg)
        elif cmd == "7":
            # 가게 내의 음식 목록 요청
            rest_num = msg_list[1]
            food_list, rest_name = self.food_server_db.select_food_data(rest_num)
            num = len(food_list)
            msg = "8//{0}//{1}//".format(num, rest_name[0][0])
            for i in range(num):
                food_list[i] = list(food_list[i])
                for j in range(2):
                    food_list[i][j] = str(food_list[i][j])
                msg = msg + "//".join(food_list[i]) + "//"
            self.send_msg(msg)
        elif cmd == "9":
            # 채팅방 입장 요청
            food_num = msg_list[1]
            info = self.food_server_db.select_food_name_data(food_num)
            rest_name, food_name = info[0]
            nick_name = msg_list[3]
            if room_info.get(food_num) is None:
                room_info[food_num] = []
            room_info[food_num].append(self.client_socket)
            num = len(room_info[food_num])
            msg = "10//{0}//{1}//{2}//{3}//{4}//".format(rest_name, food_name, num, nick_name, 1)
            self.send_msg(msg)

            # 검색 내용 추가
            user_num = msg_list[2]
            self.food_server.add_search_data(user_num, food_num)

            # 이미 방에 있는 사람들에게 입장 알림
            if num:
                msg = "10//{0}//{1}//{2}//{3}//{4}//".format(rest_name, food_name, num, nick_name, 0)
                for c_s in room_info[food_num]:
                    if c_s != self.client_socket:
                        self.send_msg_using_socket(msg, c_s)
        elif cmd == "11":
            # 메세지 전송
            food_num = msg_list[3]
            for c_s in room_info[food_num]:
                self.send_msg_using_socket(msg, c_s)
        elif cmd == "13":
            # 채팅방 나가기 요청
            # 채팅방 목록에서 제거
            food_num = msg_list[1]
            nick_name = msg_list[2]
            room_info[food_num].remove(self.client_socket)

            # 채팅방에 남아 있는 사람에 알림
            num = len(room_info[food_num])
            if num:
                msg = "14//{0}//{1}".format(num, nick_name)
                for c_s in room_info[food_num]:
                    self.send_msg_using_socket(msg, c_s)
        elif cmd == "15":
            #user top5 요청
            msg = "16//" + "//".join(self.food_server.user_top5_list[0]) + "//"
            self.send_msg(msg)
        elif cmd == "20":
            # 로그아웃
            user_num = msg_list[1]
            self.food_server.create_person_csv(user_num)
        elif cmd == "100":
            category = msg_list[1]
            user_num = int(msg_list[2])
            if category == "1":
                # 한식
                self.food_server.food_server_db.insert_search_datas(self.food_server.insert_search_data("한식", user_num, 50))
            elif category == "2":
                # 중식
                self.food_server.food_server_db.insert_search_datas(self.food_server.insert_search_data("중식", user_num, 50))
            elif category == "3":
                # 양식
                self.food_server.food_server_db.insert_search_datas(self.food_server.insert_search_data("양식", user_num, 50))
            elif category == "4":
                # 일식
                self.food_server.food_server_db.insert_search_datas(self.food_server.insert_search_data("일식", user_num, 50))
            elif category == "5":
                # 분식
                self.food_server.food_server_db.insert_search_datas(self.food_server.insert_search_data("분식", user_num, 50))
            elif category == "6":
                self.init_data(self.food_server)
            self.food_server.create_person_csv(user_num)
        else:
            self.send_msg("실패")

    def init_data(self, food_server):
        # 데이터 초기화
        self.food_server.food_server_db.delete_all_data("search")
        self.food_server.food_server_db.insert_search_datas(food_server.create_search_data(600))

        self.food_server.food_server_db.insert_search_datas(food_server.insert_search_data("한식", 1, 100))
        self.food_server.food_server_db.insert_search_datas(food_server.insert_search_data("양식", 2, 100))
        self.food_server.food_server_db.insert_search_datas(food_server.insert_search_data("중식", 3, 100))
        self.food_server.food_server_db.insert_search_datas(food_server.insert_search_data("중식", 4, 50))
        self.food_server.food_server_db.insert_search_datas(food_server.insert_search_data("양식", 4, 50))
        self.food_server.food_server_db.insert_search_datas(food_server.insert_search_data("분식", 5, 100))

        self.food_server.food_server_db.select_all_data("search")

        for i in range(6):
            self.food_server.create_person_csv(i)


    def send_msg(self, msg):
        send_msg = msg
        self.client_socket.send(send_msg.encode("euc-kr"))
        print("[SEND] : " + send_msg)

    def send_msg_using_socket(self, msg, tmp_soc):
        tmp_soc.send(msg.encode("euc-kr"))
        print("[SEND] : " + msg)



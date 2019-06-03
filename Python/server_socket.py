from socket import *
from random import *
import copy
import threading, csv
import server_db
from datetime import datetime, timedelta
import glob
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split

BUFSIZE = 128
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
            temp.append(user_num-1)
            result1.append(temp)
        result1.insert(0, title)
        self.create_csv_row(result1, "person{0}.csv".format(user_num - 1), "./data/person/")

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

    def food_analysis(self, top5_list, user_ac_list):
        input_path = "./data/person/"
        rows_num = 20
        check_percent = 0.20

        # id 로그인
        input_id = input("id를 입력 : ")
        input_id_int = int(input_id)

        # 현재 시간 전부
        currentTime = datetime.now()
        # 7일전
        currentTime7 = currentTime - timedelta(days=7)

        # 현재 시간만
        ct = currentTime.hour

        allFiles = glob.glob(input_path + "*.csv")
        print(input_path)
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

        # allData = allData.loc[(allData['Search_Time'] > currentTime7), :]

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
        # 메뉴
        menu_list = str(list(data.Menu)).strip('[]').replace("'", "").replace(",", "")

        # 전체 데이터 인코딩
        onehot_data = pd.get_dummies(data.Menu)

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
            top_count = 0
            print(str(ct) + "시 기준 탑5")
            # one hot encoding
            time_df = pd.get_dummies(timeDic[time].Menu)

            sum_time_df = pd.DataFrame(time_df.sum(axis=0), columns=["count"])
            sort_time_df = sum_time_df.sort_values(by="count", ascending=False)
            top_time_df = sort_time_df[0:5].index.tolist()

            for item in top_time_df:
                top_count += 1
                print(str(top_count) + ":" + item)
            print('----------------------------------------------')

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

        for i in temp:
            top5_list.append(i)

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

        # 취향 일치율 출력
        # for i in range(len(ac_scores)):
        #    for j in range(len(ac_scores[i])):
        #        newStr = str(i) + str(j + 1 + i) + '정답률 : '
        #        print(newStr, ac_scores[i][j])

        # 취향에 따른 추천
        def recommend(id):
            canFind = False
            print(ac_scores)
            for i in range(id):
                print(i, " > ", ac_scores[i][id - 1 - i])
                if float(ac_scores[i][id - 1 - i]) > check_percent:
                    canFind = True
                    top_count = 0
                    print(str(id) + "님과 비슷한 취향을 가진 " + str(i) + "님의 메뉴 탑5")
                    for item in personTop5Datas[i]:
                        top_count += 1
                        print(str(top_count) + ":" + item)

            if id < len(ac_scores):
                for i in range(len(ac_scores[id])):
                    print(i, " : ", ac_scores[id][i])
                    if float(ac_scores[id][i]) > check_percent:
                        canFind = True
                        top_count = 0
                        top5Index = id + i + 1
                        print(str(id) + "님과 비슷한 취향을 가진 " + str(top5Index) + "님의 메뉴 탑5")
                        for item in personTop5Datas[top5Index]:
                            top_count += 1
                            print(str(top_count) + ":" + item)

            if canFind == False:
                print(str(id) + "님과 비슷한 취향의 회원이 존재하지 않습니다.")

        recommend(input_id_int)
        """

        # 사람별 카테고리 탑5 출력
        # 카테고리 입력 및 검색어 받음
        def personal_taste(id):
            # 지역 변수
            top_count = 0
            person_df = allData.loc[allData["id"] == id]

            # 한명의 탑5 카테고리
            person_onehot_category_data = pd.get_dummies(person_df.Search_Category)
            sum_person_df = pd.DataFrame(person_onehot_category_data.sum(axis=0), columns=["count"])
            # 카테고리 기준으로 오름차순 정리
            sort_sum_person_df = sum_person_df.sort_values(by="count", ascending=False)
            top5_person_df = sort_sum_person_df[0:5].index.tolist()
            print("person" + str(id) + "님의 카테고리 탑5")

            for item in top5_person_df:
                top_count += 1
                print(str(top_count) + ":" + item)

            # 노가다 용 코드
            # searchCategory = '양식'
            # searchWord = '피자'
            

            print("---------------------------")
            #searchCategory = input('카테고리 : ')
            searchWord = input('검색어 : ')
            searchTime = currentTime

            df = pd.DataFrame(
                {"id": [id], "Search_Time": [searchTime], "Search_Category": [searchCategory],
                 "Search_Word": [searchWord]})
            result = person_df.append(df)
            result.to_csv(input_path + "person" + str(id) + ".csv", encoding="euc-kr",
                          index=False)
              

        print("---------------------------")
        # 노가다용
        # for item in range(6):
        # personal_taste(1)
        # id input
        personal_taste(input_id_int)

        print("---------------------------")"""


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

    def __init__(self, client_socket, list_client_socket):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.list_client_socket = list_client_socket
        self.food_server_db = server_db.FoodServerDB()

    def exit_receiver(self):
        self.flag = 0

    def run(self):
        while self.flag:
            try:
                print('[Now] : Waiting Msg')
                data = self.client_socket.recv(BUFSIZE)
                self.process_recv_msg(data)
                print('[Recv] : ', data.decode("euc-kr"))
            except:
                print("[Close] : ", self.client_socket)
                self.list_client_socket.remove(self.client_socket)
                break

    def process_recv_msg(self, msg):
        msg = msg.decode("euc-kr")
        msg_list = msg.split("//")
        cmd = msg_list[0]
        print("[Cmd] : " + cmd)
        if cmd == "1":
            id = msg_list[1]
            pwd = msg_list[2]
            rows = self.food_server_db.get_user_using_info(id, pwd)
            #로그인 성공
            if len(rows) == 1:
                msg = "2//1//" + str(rows[0][0]) + "//" + rows[0][1] + "//" + rows[0][2] + "//"
            else:
                msg = "2//0//"
            self.send_msg(msg)
        else:
            self.send_msg("실패")

    def send_msg(self, msg):
        send_msg = msg
        self.client_socket.send(send_msg.encode("euc-kr"))
        print("[SEND] : " + send_msg)


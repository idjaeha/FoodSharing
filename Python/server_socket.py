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
    ���ϰ� DB�� �����ϰ� ���� ��ɵ��� �����ϴ� Ŭ����
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
        Ŭ���̾�Ʈ ���� ������ ����Ʈ�� ��ȯ�մϴ�.
        """
        return self.list_client_socket

    def create_connector(self):
        """
        ���� ������ Ŀ���͸� �����մϴ�.
        """
        self.client_connector = FoodServerConnector(self.list_client_socket, self.list_client_receiver)
        self.client_connector.start()

    def exit_server(self):
        """
        ������ �����մϴ�.
        """
        for client_socket in self.list_client_receiver:
            client_socket.exit_receiver()
        print('[NOW] : Receiver Exit')
        self.client_connector.exit_connector()
        print('[NOW] : Connector Exit')

    def create_csv_row(self, data, filename="output.csv", file_location="./"):
        """
        list ���·� ���� data�� csv ���� ���·� �������ϴ�.
        data�� ����Ʈ��� �̷���������� ����Ʈ�� ù��° ���� �� ���� ������ ���մϴ�.
        filename�� ���� ������ ���� �ʴ´ٸ� output.csv �� �������� ����մϴ�.
        """
        fieldnames = []
        # ������ fieldnames�� �����մϴ�.
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
        �������� ������ �˻� ����� ������ִ� �Լ�
        :param num
        :return:
        """
        test_search = []

        example = \
            [["�ѽ�", "�����", "�Ұ��", "�����", "��ġ�", "��ġ��", "������"],
             ["�߽�", "�����", "«��", "������", "��ǳ��", "�Ⱥ�ä", "ĥ������"],
             ["���", "�Ľ�Ÿ", "������ũ", "������", "���ɷ�", "�ܹ���", "����"],
             ["�Ͻ�", "�ʹ�", "������", "�쵿", "�ٵ�", "���", "��ù�"],
             ["�н�", "������", "���", "Ƣ��", "����", "����", "�ָԹ�"]]

        temp_times = []
        # �������� �ð��� ����
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
        �������� ������ �˻� ����� �߰����ִ� �Լ�
        :param num
        :return:
        """
        test_search = []
        start_num = self.food_server_db.get_data_num("search")

        example = \
            [["�ѽ�", "�����", "�Ұ��", "�����", "��ġ�", "��ġ��", "������"],
             ["�߽�", "�����", "«��", "������", "��ǳ��", "�Ⱥ�ä", "ĥ������"],
             ["���", "�Ľ�Ÿ", "������ũ", "������", "���ɷ�", "�ܹ���", "����"],
             ["�Ͻ�", "�ʹ�", "������", "�쵿", "�ٵ�", "���", "��ù�"],
             ["�н�", "������", "���", "Ƣ��", "����", "����", "�ָԹ�"]]

        temp_times = []
        # �������� �ð��� ����
        for i in range(num):
            start = datetime.now()
            end = start + timedelta(days=7)
            temp_times.append(start + (end - start) * random())
        temp_times.sort()


        for i in range(num):
            temp = []
            temp.append(start_num + i)
            temp.append(user_num)
            temp.append(temp_times[i])
            if category == "�ѽ�":
                temp.append(randint(1, 3))
            elif category == "�߽�":
                temp.append(randint(4, 6))
            elif category == "���":
                temp.append(randint(7, 9))
            elif category == "�Ͻ�":
                temp.append(randint(10, 12))
            elif category == "�н�":
                temp.append(randint(13, 15))
            test_search.append(temp)

        return test_search

    def create_food_data(self):
        """
        �������� ���� �����͸� ������ִ� �Լ�
        :param csv_flag:
        :return:
        """
        test_food = []
        example = \
            [["�ѽ�", "�����", "�Ұ��", "�����", "��ġ�", "��ġ��", "������"],
             ["�߽�", "�����", "«��", "������", "��ǳ��", "�Ⱥ�ä", "ĥ������"],
             ["���", "�Ľ�Ÿ", "������ũ", "������", "���ɷ�", "�ܹ���", "����"],
             ["�Ͻ�", "�ʹ�", "������", "�쵿", "�ٵ�", "���", "��ù�"],
             ["�н�", "������", "���", "Ƣ��", "����", "����", "�ָԹ�"]]
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
        �������� ���� �����͸� ������ִ� �Լ�
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
        �������� ���� �����͸� ������ִ� �Լ�
        :param csv_flag:
        :return:
        """
        test_rest = []
        user_name = ["����", "��ȣ", "��ȣ", "����"]
        category = ["�ѽ�", "�߽�", "���", "�Ͻ�", "�н�"]
        sample_name = [["������", "���ֽĴ�", "������", "������", "ū��"],
                       ["�ϸ���", "�¸���", "�߱���", "��ȭ����", "�⸸��"],
                       ["��Ʋ �Ľ�Ÿ", "������ ������ũ", "������", "������ ���", "��������"],
                       ["������", "���ø���", "ȫ����", "��Ÿ��", "�ٵ�"],
                       ["������", "���õ��", "�Ѽ� �н�", "����������", "�̽��� ���", "��� �Ϲ���"]]
        rest_num = 1

        for name in user_name:
            for i in range(5):
                temp = []
                temp.append(rest_num)
                temp.append(name + "�� " + sample_name[i][randrange(len(sample_name[i]))])
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
        search ���̺� ���� �߰��ϴ� �Լ�
        :param user_num:
        :param food_num:
        :return:
        """
        num = self.food_server_db.get_data_num("search") + 1
        search_value = [num, user_num, datetime.now(), food_num]

        self.food_server_db.insert_search_data(search_value, True)

    def create_basic_table(self):
        self.food_server_db.create_table()

    def food_analysis(self, input_id_int, top5_list, user_ac_list):
        input_path = "./data/person/"
        rows_num = 80

        # ���� �ð� ����
        currentTime = datetime.now()
        # 7����
        currentTime7 = currentTime - timedelta(days=7)

        # ���� �ð���
        ct = currentTime.hour

        allFiles = glob.glob(input_path + "*.csv")
        people = len(allFiles)
        allData = pd.DataFrame()
        list_ = []
        classification_ = []
        allClassification_df = []

        # ��� ���� ������ ����
        for file_ in allFiles:
            df = pd.read_csv(file_, index_col=None, header=0, encoding="euc-kr")
            Classification_df = df[['Search_Time', 'Search_Word']]
            list_.append(df)
            classification_.append(Classification_df)

        # BestSeller ����
        allClassification_df = pd.concat(classification_)
        allData = pd.concat(list_)

        # 7�� �̻�� row ����
        allData['Search_Time'] = pd.to_datetime(allData['Search_Time'])

        # �ð� �з�
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

        # �޴��� �ð��� �޴� �����ͻ���
        data = pd.DataFrame({'Time': Time,
                             'Menu': Menu})

        # ������ �ð��� ��¥ ���� list ����
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

        # �ð����� �ٷ�� list ����
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
                # ���0�� ������ �м�
                person_df = allData.loc[allData["id"] == i]
                person_search_df = person_df[["Search_Category", "Search_Word"]]
                person_onehot_search_word_data = pd.get_dummies(person_search_df.Search_Word)

                # ���0�� ž5 �޴�
                sum_person_df = pd.DataFrame(person_onehot_search_word_data.sum(axis=0), columns=["count"])
                sort_sum_person_df = sum_person_df.sort_values(by="count", ascending=False)
                top5_person_df = sort_sum_person_df[0:5].index.tolist()

                person_data = person_onehot_search_word_data
                person_label = person_df[["Search_Category"]]

                # �н� ���� �����Ϳ� �׽�Ʈ ���� �����ͷ� ������
                person_data_train, person_data_test, person_label_train, person_label_test = train_test_split(
                    person_data,
                    person_label,
                    test_size=rows_num)
                personList.append(person_label_test)
                top5List.append(top5_person_df)

            return personList

        personTop5Datas = []
        personDatas = addPersonData(personTop5Datas, people)

        # �н�, ����

        # ����� ���� ��ġ��
        ac_scores = []
        for i in range(len(personDatas)):
            scoreList = []
            for j in range((len(personDatas) - 1) - i):
                scoreList.append(metrics.accuracy_score(personDatas[i], personDatas[j + 1 + i]))
            if len(scoreList) != 0:
                ac_scores.append(scoreList)

        # ���⿡ ���� ��õ
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
        �ǽð� �˻� top5_list�� ���ڷ� ���� ���� ���⿡ ���� top5�� ���� �� �ִ� �޼���
        flag�� False�� �ϰ� �Ǹ� �ش� ������ db���� �Ѿ�� �ʴ´�.
        :param user_num: 
        :param flag: 
        :return: 
        """
        self.food_analysis(int(user_num), self.top5_list, self.user_top5_list)
        if flag:
            self.food_server_db.update_user_top5(user_num, self.user_top5_list[0])


class FoodServerConnector(threading.Thread):
    """
    Ŭ���̾�Ʈ���� ������ ���� ����ϴ� Ŀ����
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
        # ���� ����
        _server_socket = socket(AF_INET, SOCK_STREAM)

        # ���� �ּ� ���� �Ҵ�
        _server_socket.bind(ADDR)
        print('[Now] : Bind')

        # ���� ���� ��� ����(���� ���� �� ����� ������ ����� ������ ����)
        _server_socket.listen(100)
        while self.flag:
            # ���� ����
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
    Ŭ���̾�Ʈ���� �޼����� �ޱ� ���� ����ϴ� ���ù�
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
            # ���� ���� ����
            self.send_msg("0//")
        elif cmd == "1":
            # �α��� ����, ����
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
            # top5 ����Ʈ ����
            self.food_server.update_user_top5(0, False)
            top5_msg = "4//" + "//".join(self.food_server.top5_list[0]) + "//"
            self.send_msg(top5_msg)
        elif cmd == "5":
            # �Ĵ� �ڷ� ��û
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
            # ���� ���� ���� ��� ��û
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
            # ä�ù� ���� ��û
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

            # �˻� ���� �߰�
            user_num = msg_list[2]
            print(msg_list)
            self.food_server.add_search_data(user_num, food_num)
            print(msg_list[2])

            # �̹� �濡 �ִ� ����鿡�� ���� �˸�
            if num:
                msg = "10//{0}//{1}//{2}//{3}//{4}//".format(rest_name, food_name, num, nick_name, 0)
                print("msg")
                for c_s in room_info[food_num]:
                    if c_s != self.client_socket:
                        self.send_msg_using_socket(msg, c_s)
        elif cmd == "11":
            # �޼��� ����
            food_num = msg_list[3]
            for c_s in room_info[food_num]:
                self.send_msg_using_socket(msg, c_s)
        elif cmd == "13":
            # ä�ù� ������ ��û
            # ä�ù� ��Ͽ��� ����
            food_num = msg_list[1]
            nick_name = msg_list[2]
            room_info[food_num].remove(self.client_socket)

            # ä�ù濡 ���� �ִ� ����� �˸�
            num = len(room_info[food_num])
            if num:
                msg = "14//{0}//{1}".format(num, nick_name)
                for c_s in room_info[food_num]:
                    self.send_msg_using_socket(msg, c_s)
        elif cmd == "15":
            #user top5 ��û
            msg = "16//" + "//".join(self.food_server.user_top5_list[0]) + "//"
            self.send_msg(msg)
        elif cmd == "20":
            # �α׾ƿ�
            user_num = msg_list[1]
            self.food_server.create_person_csv(user_num)
        elif cmd == "100":
            category = msg_list[1]
            user_num = int(msg_list[2])
            if category == "1":
                # �ѽ�
                self.food_server.food_server_db.insert_search_data(self.food_server.insert_search_data("�ѽ�", user_num, 50))
            elif category == "2":
                # �߽�
                self.food_server.food_server_db.insert_search_data(self.food_server.insert_search_data("�߽�", user_num, 50))
            elif category == "3":
                # ���
                self.food_server.food_server_db.insert_search_data(self.food_server.insert_search_data("���", user_num, 50))
            elif category == "4":
                # �Ͻ�
                self.food_server.food_server_db.insert_search_data(self.food_server.insert_search_data("�Ͻ�", user_num, 50))
            elif category == "5":
                # �н�
                self.food_server.food_server_db.insert_search_data(self.food_server.insert_search_data("�н�", user_num, 50))
            elif category == "6":
                self.init_data(self.food_server)
            self.food_server.create_person_csv(user_num)
        else:
            self.send_msg("����")

    def init_data(self, food_server):
        # ������ �ʱ�ȭ
        self.food_server.food_server_db.delete_all_data("search")
        self.food_server.food_server_db.insert_search_data(food_server.create_search_data(600))

        self.food_server.food_server_db.insert_search_data(food_server.insert_search_data("�ѽ�", 1, 100))
        self.food_server.food_server_db.insert_search_data(food_server.insert_search_data("���", 2, 100))
        self.food_server.food_server_db.insert_search_data(food_server.insert_search_data("�߽�", 3, 100))
        self.food_server.food_server_db.insert_search_data(food_server.insert_search_data("�߽�", 4, 50))
        self.food_server.food_server_db.insert_search_data(food_server.insert_search_data("���", 4, 50))
        self.food_server.food_server_db.insert_search_data(food_server.insert_search_data("�н�", 5, 100))

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



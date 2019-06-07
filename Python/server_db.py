#-*- coding: euc-kr -*-

import sqlite3


class FoodServerDB:
    conn = 0
    cur = 0

    def __init__(self):
        pass

    def create_table(self):
        """
        기본적인 푸드쉐어링 DB와 테이블을 생성합니다.
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()

        # Create table
        self.cur.execute('''CREATE TABLE rest
                                     (rest_num INTEGER PRIMARY KEY, rest_name text, category text, x real , y real)''')

        self.cur.execute('''CREATE TABLE food
                                     (food_num INTEGER PRIMARY KEY, rest_num INTEGER , category text, food_name text)''')

        self.cur.execute('''CREATE TABLE user
                             (user_num INTEGER PRIMARY KEY, id text, pwd text, food1 INTEGER, food2 INTEGER,food3 INTEGER, food4 INTEGER, food5 INTEGER)''')

        self.cur.execute('''CREATE TABLE search
                                             (search_num INTEGER PRIMARY KEY, user_num INTEGER , time text, food_num INTEGER   )''')

        # Save (commit) the changes
        self.conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.conn.close()

    def insert_restaurant_data(self, values):
        """
        해당 테이블에 데이터를 넣습니다.
        :param values:
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()

        sql = "INSERT INTO rest VALUES (?, ?, ?, ?, ?)"
        self.cur.execute(sql, values)
        #많은 데이터를 넣고자 할때 사용
        #self.cur.executemany(sql, values)

        self.conn.commit()
        self.conn.close()

    def insert_food_data(self, values):
        """
        해당 테이블에 데이터를 넣습니다.
        :param values:
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()

        sql = "INSERT INTO food VALUES (?, ?, ?, ?)"
        self.cur.execute(sql, values)
        #많은 데이터를 넣고자 할때 사용
        #self.cur.executemany(sql, values)

        self.conn.commit()
        self.conn.close()

    def insert_user_data(self, values):
        """
        해당 테이블에 데이터를 넣습니다.
        (user_num INTEGER PRIMARY KEY, id text, pwd text,
        food1 INTEGER, food2 INTEGER,food3 INTEGER, food4 INTEGER, food5 INTEGER)
        :param values:
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()

        sql = "INSERT INTO user VALUES (?, ?, ?, ?, ?, ? ,? ,?)"
        #self.cur.execute(sql, values)
        #많은 데이터를 넣고자 할때 사용
        self.cur.executemany(sql, values)

        self.conn.commit()
        self.conn.close()

    def insert_search_data(self, values):
        """
        해당 테이블에 데이터를 넣습니다.
        :param values:
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()

        sql = "INSERT INTO search VALUES (?, ?, ?, ?)"
        self.cur.execute(sql, values)
        self.conn.commit()
        self.conn.close()

    def insert_search_datas(self, values):
        """
        해당 테이블에 데이터를 넣습니다.
        (user_num INTEGER PRIMARY KEY, id text, pwd text,
        food1 INTEGER, food2 INTEGER,food3 INTEGER, food4 INTEGER, food5 INTEGER)
        :param values:
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()
        sql = "INSERT INTO search VALUES (?, ?, ?, ?)"
        #self.cur.execute(sql, values)
        #많은 데이터를 넣고자 할때 사용
        self.cur.executemany(sql, values)

        self.conn.commit()
        self.conn.close()

    def select_human_csv(self, user_num):
        """
        분석 인풋 형식에 맞는 데이터를 뽑아냅니다.
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()
        sql = "select f.category, s.time, f.food_name from food f, search s where s.user_num = ? and s.food_num = f.food_num"
        self.cur.execute(sql, (user_num, ))
        self.conn.commit()

        rows = self.cur.fetchall()

        self.conn.close()
        return rows

    def select_all_data(self, table):
        """
        테이블에서 모든 데이터를 읽어옵니다.
        인자의 형식은 스트링으로 받습니다.
        :param table:
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()
        sql = "select * from {0}".format(table)
        self.cur.execute(sql)
        self.conn.commit()

        rows = self.cur.fetchall()
        for row in rows:
            print(row)

        self.conn.close()

    def delete_all_data(self, table):
        """
        table에 모든 데이터를 삭제합니다.
        :param table:
        :return:
        """

        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()
        sql = "DELETE from " + table
        self.cur.execute(sql)

        self.conn.commit()
        self.conn.close()

    def select_rest_data(self, category, flag=False):
        """
        rest 데이터를 가져옵니다.
        :param category:
        :return:
        """
        if not flag:
            self.conn = sqlite3.connect('./data/db/FoodSharing.db')
            self.cur = self.conn.cursor()
            sql = "select * from rest where category = '{0}'".format(category)
            #sql = "select * from rest"
            self.cur.execute(sql)
            self.conn.commit()

            rows = self.cur.fetchall()
            self.conn.close()

            return rows
        else:
            self.conn = sqlite3.connect('./data/db/FoodSharing.db')
            self.cur = self.conn.cursor()
            sql = "select r.* from rest r, food f where f.rest_num = r.rest_num and f.food_name = '{0}'".format(category)
            if (flag):
                print(sql)
            self.cur.execute(sql)
            self.conn.commit()

            rows = self.cur.fetchall()
            self.conn.close()

            return rows

    def get_data_num(self, table):
        # 테이블 안의 데이터에 개수를 가져옵니다.
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()

        sql = "select * from {0}".format(table)
        self.cur.execute(sql)
        num = len(self.cur.fetchall())

        self.conn.commit()
        self.conn.close()
        return num

    def get_user_using_info(self, id, pwd):
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()
        try:
            sql = "select * from user where id = '{0}' and pwd = '{1}'".format(id, pwd)
            self.cur.execute(sql)
        except:
            self.conn.close()
            return []

        rows = self.cur.fetchall()

        self.conn.commit()
        self.conn.close()
        return rows

    def update_user_top5(self, user_num, top5_list):
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()
        try:
            sql = "update user set food1 = '{0}' where user_num = {1}".format(top5_list[0], user_num)
            self.cur.execute(sql)
            sql = "update user set food2 = '{0}' where user_num = {1}".format(top5_list[1], user_num)
            self.cur.execute(sql)
            sql = "update user set food3 = '{0}' where user_num = {1}".format(top5_list[2], user_num)
            self.cur.execute(sql)
            sql = "update user set food4 = '{0}' where user_num = {1}".format(top5_list[3], user_num)
            self.cur.execute(sql)
            sql = "update user set food5 = '{0}' where user_num = {1}".format(top5_list[4], user_num)
            self.cur.execute(sql)
        except:
            self.conn.close()
            return []

        rows = self.cur.fetchall()

        self.conn.commit()
        self.conn.close()
        return rows

    def select_food_data(self, rest_num):
        """
        food data를 food_num 과 food_name으로 가져옵니다.
        :param rest_num:
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()
        sql = "select food_num, food_name from food where rest_num = '{0}'".format(rest_num)
        self.cur.execute(sql)
        self.conn.commit()

        rows = self.cur.fetchall()

        sql = "select rest_name from rest where rest_num = '{0}'".format(rest_num)
        self.cur.execute(sql)
        self.conn.commit()

        name = self.cur.fetchall()

        self.conn.close()

        return rows, name

    def select_food_name_data(self, food_num):
        """
        food num을 통해 rest_num 과 food_num을 가져옵니다.
        :param food_num:
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()
        sql = sql = "select r.rest_name, f.food_name from rest r, food f where f.rest_num = r.rest_num and f.food_num = '{0}'".format(food_num)
        self.cur.execute(sql)
        self.conn.commit()

        rows = self.cur.fetchall()

        self.conn.close()

        return rows

    def select_user_top5_data(self, user_num):
        """
        food num을 통해 rest_num 과 food_num을 가져옵니다.
        :param food_num:
        :return:
        """
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()
        sql = sql = "select food1, food2, food3, food4, food5 from user where user_num = '{0}'".format(user_num)
        self.cur.execute(sql)
        self.conn.commit()

        rows = self.cur.fetchall()

        self.conn.close()

        return rows



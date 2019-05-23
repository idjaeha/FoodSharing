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
        self.cur.execute(sql, values)
        #많은 데이터를 넣고자 할때 사용
        #self.cur.executemany(sql, values)

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
        #많은 데이터를 넣고자 할때 사용
        #self.cur.executemany(sql, values)

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
        for row in rows:
            print(row)

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

    def execute_sql(self, sql):
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()

        self.cur.execute(sql)

        self.conn.commit()
        self.conn.close()

    def get_data_num(self, table):
        self.conn = sqlite3.connect('./data/db/FoodSharing.db')
        self.cur = self.conn.cursor()

        sql = "select * from {0}".format(table)
        self.cur.execute(sql)
        num = len(self.cur.fetchall())

        self.conn.commit()
        self.conn.close()
        return num


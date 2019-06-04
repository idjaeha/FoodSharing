#-*- coding: euc-kr -*-

import server_socket


def run():
    food_server = server_socket.FoodServer()
    food_server.create_connector()
"""
    top5_list = []
    user_ac_list = []
    food_server.food_analysis(1, top5_list, user_ac_list)
    print(top5_list)
    print(user_ac_list)
    """





if __name__ == '__main__':
    run()

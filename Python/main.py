#-*- coding: euc-kr -*-

import server_socket


def run():
    food_server = server_socket.FoodServer()
    #init_data(food_server)
    food_server.create_connector()

if __name__ == '__main__':
    run()

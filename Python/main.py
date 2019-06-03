import server_socket


def run():
    food_server = server_socket.FoodServer()
    top5_list = []
    user_ac_list = []
    while 1:
        food_server.food_analysis(top5_list, user_ac_list)
        print(top5_list)
        print(user_ac_list)

   # food_server.create_connector()




if __name__ == '__main__':
    print(run())

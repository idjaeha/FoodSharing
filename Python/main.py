import server_socket


def run():
    food_server = server_socket.FoodServer()
    food_server.create_connector()

    while 1:
        send_msg = input("Enter the msg : ")
        for i in food_server.list_client_socket:
            i.send(send_msg.encode("euc-kr"))



if __name__ == '__main__':
    print(run())

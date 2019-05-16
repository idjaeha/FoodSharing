import server_socket


def run():
    food_server = server_socket.FoodServer()
    food_server.create_connector()
    while True:
        msg = input('Enter the Msg : ')
        if msg == 'exit':
            food_server.exit_server()
            return 0


if __name__ == '__main__':
    print(run())

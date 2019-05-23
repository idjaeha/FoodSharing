import server_socket


"""
food_server.create_sample_csv(["한식","비빔밥","불고기","된장찌개","김치찌개","김치전","떡갈비"],
                              ["중식","자장면","짬뽕","탕수육","깐풍기","팔보채","칠리새우"],
                              ["양식","파스타","스테이크","샐러드","오믈렛","햄버거","피자"],
                              ["일식","초밥","가츠동","우동","텐동","라멘","사시미"],
                              ["분식","떡볶이","김밥","튀김","순대","오뎅","주먹밥"])
"""


def run():
    food_server = server_socket.FoodServer()
    #food_server.food_server_db.insert_search_data(food_server.create_search_data())
    food_server.food_server_db.select_all_data("rest")
    food_server.food_server_db.select_all_data("food")
    food_server.food_server_db.select_all_data("user")
    food_server.food_server_db.select_all_data("search")






if __name__ == '__main__':
    print(run())

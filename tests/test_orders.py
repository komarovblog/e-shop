from fastapi.testclient import TestClient
from main import app
from db.connect_db import database_connect_no_async
from orders.order_structure import MakeOrder

# При иморте файла вот так import main, в данном случае main, он импортируется как модуль и можно вызывать функции из файла через точку, например main.app, но в данном случае мы сделали вот так from main import app, поэтому точка не нужна.

# Для тестов клиент это не пользователь, а объект, который будет посылвать запросы на сервер. Этот объект как раз и есть TestClient, он нужен ТОЛЬКО для тестирования запросов. Для теста просто функцияй такое не нужно.

client = TestClient(app)

# Теперь мы можем тестировать функции из мэйн таким удобным способом и функция сразу вернет ответ.
def test_orders():

    connection = database_connect_no_async.get_connection()
    cursor = connection.cursor()

    cursor.execute ("DELETE FROM products; DELETE FROM users; DELETE FROM orders; DELETE FROM products_link_orders")
    connection.commit()

    cursor.execute(
        """
        INSERT INTO products (name, price, volume, color, is_active) VALUES ('Красный', 100, 1, 'red', True);
        INSERT INTO products (name, price, volume, color, is_active) VALUES ('Оранжевый', 200, 1, 'orange', True);
        INSERT INTO products (name, price, volume, color, is_active) VALUES ('Желтый', 300, 1, 'yellow', True);
        """
        ) 

    cursor.execute("INSERT INTO products (name, price, volume, color, is_active) VALUES ('Зеленый', 400, 1, 'green', True) RETURNING id, name")                  
    tovar_1 = cursor.fetchall()[0][0]
    print("Выводим tovar_1")
    print(tovar_1)

    cursor.execute("INSERT INTO products (name, price, volume, color, is_active) VALUES ('Синий', 500, 1, 'blue', True) RETURNING id, name")                   
    tovar_2 = cursor.fetchall()[0][0]
    print("Выводим tovar_2")
    print(tovar_2)

    cursor.execute("INSERT INTO products (name, price, volume, color, is_active) VALUES ('Черный', 600, 1, 'black', True) RETURNING id, name")                   
    tovar_3 = cursor.fetchall()[0][0]
    print("Выводим tovar_3")
    print(tovar_3)

    cursor.execute("INSERT INTO products (name, price, volume, color, is_active) VALUES ('Белый', 700, 1, 'white', True) RETURNING id, name")  
    tovar_4 = cursor.fetchall()[0][0]
    print("Выводим tovar_4")
    print(tovar_4)

    connection.commit()

# ############################################################################

    list_pro1 = [
        {
          "id": tovar_1,
          "count": 2  
        },
        {
          "id": tovar_2,
          "count": 8  
        }
    ]
    print(list_pro1)

    make_order_1 = {
            "name" : "Альберт",
            "phone" : "8999888-77-66",
            "list_id_prod": list_pro1
        }
    print(make_order_1)

    # Сделать заказ и добавить пользователя - №1
    res = client.post("/api/order", json =  make_order_1) 
    print(res.json())


    list_pro2 = [
        {
          "id": tovar_3,
          "count": 3  
        },
        {
          "id": tovar_4,
          "count": 5  
        }
    ]
    print(list_pro2)

    make_order_2 = {
            "name" : "Альберт",
            "phone" : "8999888-77-66",
            "list_id_prod": list_pro2
        }
    print(make_order_2)

    # Сделать заказ и добавить пользователя - №2
    res = client.post("/api/order", json =  make_order_2) 
    print(res.json())

# ############################################################################

    cursor.execute("SELECT id FROM orders WHERE phone = '8999888-77-66'")
    order_id_now = cursor.fetchall()
    print("Выводим order_id_now")
    print(order_id_now)

    cursor.execute("SELECT key FROM users WHERE phone = '8999888-77-66'")
    key_user = cursor.fetchall()
    print("Выводим key_user")
    print(key_user)

    # Показать заказ по ID заказа
    res = client.get(f"/api/order/{order_id_now[0][0]}", headers = {'key': key_user[0][0]})
    print("res.json()")
    print(res.json())

# ############################################################################

    cursor.execute("SELECT id FROM users WHERE phone = '8999888-77-66'")
    user_id_now = cursor.fetchall()
    print("Выводим user_id_now")
    print(user_id_now)
    print(str(user_id_now[0][0]))

    cursor.execute("SELECT key FROM users WHERE phone = '8999888-77-66'")
    key_user = cursor.fetchall()
    print("Выводим key_user")
    print(key_user)

   # Показать все заказы пользователя по ID пользователя
    res = client.get(f"/api/order/all", headers = {'user-id': str(user_id_now[0][0]),'key': key_user[0][0]})

    print("Выводим res.json() в test_orders")
    print(res.json())

    cursor.close()
    connection.close()
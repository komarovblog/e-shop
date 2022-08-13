from fastapi.testclient import TestClient
from main import app
from db.connect_db import database_connect_no_async
from products.product_structure import EnableDisableProd, SingleProduct
from fastapi import Request


# Для тестов клиент это не пользователь, а объект, который будет посылвать запросы на сервер. Этот объект как раз и есть TestClient, он нужен ТОЛЬКО для тестирования запросов. Для теста просто функцияй такое не нужно.

client = TestClient(app)

# Теперь мы можем тестировать функции из мэйн таким удобным способом и функция сразу вернет ответ.
def test_users():
    connection = database_connect_no_async.get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM users; DELETE FROM products")
    connection.commit()

    cursor.execute(
        """
        INSERT INTO users (access, name, login, password, phone, key) 
        VALUES ('admin', 'Admin', 'admin', 'admin', 'None', 'None') 
        RETURNING id, access, name, login, password, phone, key
        """
        )   
    connection.commit()

# ############################################################################

    # Авторизоваться
    print ("# Авторизоваться")
    res = client.post("/api/sign_in", headers = {'login': 'admin', 'password': 'admin'}) 
    print (res.status_code)
    print(res.json())
 
# ############################################################################

    cursor.execute("SELECT key FROM users WHERE login = 'admin'")  
    key_now = cursor.fetchall()[0][0] 
 
    lsit_single_prod = [
        {
            "name" : "Новый-1",
            "price" : 800,
            "volume": 8,
            "color": "black"
        },
        {
            "name" : "Новый-2",
            "price" : 900,
            "volume": 9,
            "color": "red"
        },
    ]

    # Добавить товары
    print ("# Добавить товары")
    res = client.post("/api/admin/add_products", json = lsit_single_prod, headers = {'key': key_now}) 
    print (res.status_code)
    print(res.json())

    cursor.execute(f"SELECT * FROM products")
    prod_now = cursor.fetchall()
    print(prod_now)

# ############################################################################

    print ("Внимание ключ") 
    cursor.execute("SELECT key FROM users WHERE login = 'admin'")  
    key_now = cursor.fetchall()[0][0] 
    print(key_now)

    cursor.execute("SELECT id FROM products p WHERE p.name = 'Новый-1'")
    id_now = cursor.fetchall()[0][0]
    print ("Внимание id")
    print(id_now)

    new_param_prod = '{"name": "Измененный-1"}'

    # Редактировать товар
    print ("# Редактировать товар")
    res = client.put(f"/api/admin/edit_product/{id_now}", data = new_param_prod, headers = {'key': key_now})

    print ("Внимание изменили") 
    print (res.status_code)
    print(res.json())
    cursor.execute(f"SELECT * FROM products")
    prod_now = cursor.fetchall()
    print(prod_now)

# ############################################################################

    cursor.execute("SELECT key FROM users WHERE login = 'admin'")  
    key_now = cursor.fetchall()[0][0] 
    print(key_now)

    cursor.execute("SELECT id FROM products")
    list_id = cursor.fetchall()
    
    print ("Внимание список id")
    print(list_id)

    # list_id_now_v1 = f'{"prod_id": [{list_id[0][0]}, {list_id[1][0]}], "status": "Disable"}'

    print ("Внимание список id now")

    list_id_now_v2 = {
            "prod_id" : [list_id[0][0], list_id[1][0]],
            "status" : "Disable"
        }

    print(list_id_now_v2)

    # Включить и выключить список товаров
    print ("# Включить и выключить список товаров")
    res = client.put(f"/api/admin/products", json = list_id_now_v2, headers = {'key': key_now}) 
    print (res.status_code)
    print(res.json())

    cursor.execute(f"SELECT * FROM products")
    prod_now = cursor.fetchall()

    print("Продукты Disable")
    print(prod_now)

# ############################################################################

    # Выйти из аккаунта
    res = client.post("/api/sign_out", headers = {'key': key_now}) 
    print (res.status_code)
    print(res.json())

    cursor.close()
    connection.close()

from fastapi.testclient import TestClient
from main import app
from db.connect_db import database_connect_no_async
from products.products_work_with_db import products_work_with_db
from products.product_structure import Filter

# При иморте файла вот так import main, в данном случае main, он импортируется как модуль и можно вызывать функции из файла через точку, например main.app, но в данном случае мы сделали вот так from main import app, поэтому точка не нужна.

# Для тестов клиент это не пользователь, а объект, который будет посылвать запросы на сервер. Этот объект как раз и есть TestClient, он нужен ТОЛЬКО для тестирования запросов. Для теста просто функцияй такое не нужно.

client = TestClient(app)

# Теперь мы можем тестировать функции из мэйн таким удобным способом и функция сразу вернет ответ.
def test_products():

    connection = database_connect_no_async.get_connection()
    cursor = connection.cursor()

    cursor.execute ("DELETE FROM products")
    connection.commit()

    cursor.execute(
        """
        INSERT INTO products (name, price, volume, color, is_active) VALUES ('Красный', 100, 1, 'red', 'Enable');
        INSERT INTO products (name, price, volume, color, is_active) VALUES ('Оранжевый', 200, 1, 'orange', 'Enable');
        INSERT INTO products (name, price, volume, color, is_active) VALUES ('Желтый', 300, 1, 'yellow', 'Enable');
        INSERT INTO products (name, price, volume, color, is_active) VALUES ('Зеленый', 400, 1, 'green', 'Enable');
        INSERT INTO products (name, price, volume, color, is_active) VALUES ('Синий', 500, 1, 'blue', 'Enable');
        INSERT INTO products (name, price, volume, color, is_active) VALUES ('Черный', 600, 1, 'black', 'Enable');
        INSERT INTO products (name, price, volume, color, is_active) VALUES ('Белый', 700, 1, 'white', 'Enable')
        """
        ) 
    connection.commit()

# ############################################################################
# В json передаем словарь а не json, а в  тело (data) передаем строку, а json это и есть строка.

    print(f"Внимание!")

    request_json_v1 = "{}" # Этот json пустой, так как из него FastApi сделает BaseModel у которого есть по умолчанию поля.
    request_json_v2 = '{"name": null, "price_min": null, "price_max": null, "page_number": 1 "prod_on_page": 7}'

    # Фильтрация
    res = client.get("/api/products", data = request_json_v1) 
    print(res.json())
    assert len(res.json()['products']) == 7
    print(len(res.json()))

    # Фильтрация
    res = client.get("/api/products?price_max=500", data = '{"price_max": 500}')  
    print(res.json())
    assert len(res.json()['products']) == 5
    print(len(res.json()))
    
    # Фильтрация
    res = client.get("/api/products?name=ел&price_min=200&price_max=500", data = '{"name": "ел", "price_min": 200, "price_max": 500}')  
    print(res.json())
    assert len(res.json()['products']) == 2
    print(len(res.json()))

# ############################################################################
    print(f"Внимание!")

    # Показать товар по ID товара
    cursor.execute("SELECT * FROM products")
    sql_response = cursor.fetchall()[0][0]

    res = client.get(f"/api/products/{sql_response}") 
    print(res.json())
    assert len(res.json()) == 6 # ТУТ ВРОДЕ 1 ДОЛЖНА БЫТЬ
    print(len(res.json()))

# ############################################################################

    cursor.close()
    connection.close()
    
    # client.post('/products', json=[{...}, ])
    # client.post('/products', json=[{...}], headers={'key': 'blablabla'})
    # resp = cleint.post('/login', json={'login': .... } )

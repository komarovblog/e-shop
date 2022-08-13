# Абсолютный путь начинает из корня проекта и из той же папки из которой буду запускать.
from csv import list_dialects
from db.connect_db import database_connect

# Относительный путь иморт из текущий папки, из той в котором текущий файл
from orders.order_structure import Order, ProductInOrder
from products.product_structure import Product
from products.product_structure import SingleProduct
from products.products_work_with_db import products_work_with_db
from users.user_structure import User
from users.user_work_with_db import user_work_with_db
from orders.order_structure import MakeOrder
from orders.order_structure import OrderBaseModel

class OrderRepository:

    # Вносит в базу данные о новом заказе
    async def make_order(self, data_order: MakeOrder) -> list[tuple]:
        """Вносит в базу данные о новом заказе
        """
        connection = await database_connect.get_connection()
        user_id = await connection.fetch(f"SELECT id FROM users WHERE phone = '{data_order.phone}'")

        if len(user_id) != 0:
            order_id = await connection.fetch(f"INSERT INTO orders (status, phone, user_id) VALUES ('new', '{data_order.phone}', {user_id[0][0]}) RETURNING id")
        else:
            new_us = await user_work_with_db.add_user_customer(data_order.name, data_order.phone)
            order_id = await connection.fetch(f"INSERT INTO orders (status, phone, user_id) VALUES ('new', '{data_order.phone}', {new_us[0][0]}) RETURNING id")

        for i in data_order.list_id_prod:
            await connection.fetch(f"INSERT INTO products_link_orders (order_id, prod_id, count) VALUES ({order_id[0][0]}, {i.id}, {i.count})")
        
        await connection.close()
        return order_id


    # Возвращает один заказ по order_id
    async def show_order(self, order_id) -> Order:
        """Возвращает один заказ по order_id
        """
        connection = await database_connect.get_connection()

        sql_request = f"""
        SELECT o.id, plo.prod_id, p.price, plo.count, o.phone, o.user_id, p.name 
        FROM orders o 
        LEFT JOIN products_link_orders plo ON o.id = plo.order_id
        LEFT JOIN products p ON plo.prod_id = p.id   
        WHERE o.id = {order_id}
        """
        print(sql_request)

        result = await connection.fetch(sql_request)
        for i in result:
            print(i)

        prod_in_order = []
        for i in range(len(result)):
            prod_in_order.append(ProductInOrder(id = result[i][1], name = result[i][6], price = result[i][2], count = result[i][3]))

        order = Order(result[0][0], "new", result[0][4], result[0][5], prod_in_order)
        print(order) 

        await connection.close()
        return order 

    # Возвращает все заказы пользователя по user_id
    async def show_all_orders(self, user_id) -> list[OrderBaseModel]:
        """Возвращает все заказы пользователя по user_id
        """
        connection = await database_connect.get_connection()

        sql_request = (f""" 
        SELECT o.id, 
        MIN(o.status), 
        MIN(o.phone), 
        ARRAY_AGG(ROW(p.id, p.name, p.price, plo.count, p.price * plo.count)),
        SUM(p.price * plo.count)
        FROM orders o
        LEFT JOIN products_link_orders plo ON o.id = plo.order_id
        LEFT JOIN products p ON plo.prod_id = p.id  
        WHERE o.user_id = {user_id}
        GROUP BY o.id
        """)
     
        print("Текст запроса")
        print(sql_request)

        sql_fetchal = await connection.fetch(sql_request)

        print("Выводим ответ")
        for row in sql_fetchal:
            print(row)
            for i in row:
                print (i)

        result = []
        for row in sql_fetchal:
            prod_list_in_order = []
            for prod in row[3]:
                prod_list_in_order.append(ProductInOrder(
                                                        id = int(prod[0]), 
                                                        name = prod[1], 
                                                        price = float(prod[2]), 
                                                        count = int(prod[3]))
                                                        )
            
            result.append(OrderBaseModel(id = row[0], status = row[1], phone = row[2], user_id = user_id, prod_in_order = prod_list_in_order))        

        print("Результат")
        for order in result:
            for pro in order.prod_in_order:
                print(pro.name) 

        print("End")   
        await connection.close()
        return result

order_work_with_db = OrderRepository()
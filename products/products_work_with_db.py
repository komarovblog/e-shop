# Абсолютный путь начинает из корня проекта и из той же папки из которой будузапускать.
from db.connect_db import database_connect
from pydantic import BaseModel

# Относительный путь начинает из текущий папки, из той в котором текущий файл.
from .product_structure import Product, SingleProduct, Filter, ColorEnum, ListNewProducts, EnableDisableProd
import math


class ProductRepository:

    # Получает из базы, фильрует товары и возврвщает список
    async def get_products (self, filter: Filter) -> list[tuple]:
        """Получает товары из базы, фильрует товары и возврвщает список
        """
        connection = await database_connect.get_connection()

        criterion = []     
        sql_request = f"SELECT id, name, price, volume, color, is_active FROM products"
        
        if filter.name is not None:
            criterion.append(f"name LIKE '%{filter.name}%'")   

        if filter.price_min is not None:
            criterion.append(f"price >= {filter.price_min}")
       
        if filter.price_max is not None:
            criterion.append(f"price <= {filter.price_max}")
           
        if len(criterion) > 0:
            sql_request = f"{sql_request} WHERE "   

        result = await connection.fetch(sql_request + " and ".join(criterion) + f" LIMIT {filter.prod_on_page} OFFSET {(filter.page_number - 1) * filter.prod_on_page};")

        await connection.close()
        return result


    # Конвертирует ответ из БД в объекты.  
    def convert_products_in_list_object(self, list_db) -> list[Product]: 
        """Конвертирует ответ из БД в объекты Product, возвращает список
        """        
        list_of_products = []
        for i in list_db:
            list_of_products.append(Product(
                                            id = i[0],
                                            name = i[1], 
                                            price = i[2], 
                                            volume = i[3], 
                                            color = i[4],
                                            is_active = i[5]
                                            ))
        return list_of_products


    # Возвращает кол-во страниц - Пагинация
    def make_pagination(self, filter: Filter, list_prod: list) -> int:
        """Возвращает кол-во страниц для пагинации. На вход получает объект, Filter  
        """   
        products_on_pages = filter.prod_on_page
        count_pages = math.ceil(len(list_prod) / products_on_pages)
        return count_pages


    # Вносит в базу данных продукт принимая в аргументах объект продукта или список продуктов.
    async def insert_product(self, list_new_products: list[SingleProduct]) -> None:
        """Вносит продукт в базу данных при создании нового продукта
        """   
        connection = await database_connect.get_connection()

        for product in list_new_products:
            await connection.fetch(f"""
            INSERT INTO products (name, price, volume, color, is_active) 
            VALUES ('{product.name}', {product.price}, {product.volume}, '{product.color}', '{product.is_active}')""")

        await connection.close()


    # Редактирует товар 
    async def edit_product(self, prod_id: str, new_params: SingleProduct) -> bool:
        """Вносит изменения о продукте в базу данных при редактировании продукта
        """   
        connection = await database_connect.get_connection()
        sql_request = f"UPDATE products SET "
        
        sql_set = []
        if new_params.name is not None:
            sql_set.append (f"name = '{new_params.name}'")
        if new_params.price is not None:
            sql_set.append (f"price = {new_params.price}")
        if new_params.volume is not None:
            sql_set.append (f"volume = {new_params.volume}")
        if new_params.color is not None:
            sql_set.append (f"color = '{new_params.color}'")
        if new_params.is_active is not None:
            sql_set.append (f"is_active = '{new_params.is_active}'")

        if len(sql_set) == 0:
            return False

        await connection.fetch(sql_request + ", ".join(sql_set) + f" WHERE id = {prod_id}" )
        await connection.close()

        return True


    # Делает товар активным или не активным.
    async def enable_disable_product(self, list_of_products: EnableDisableProd) -> None:
        """Делает товар активным или не активным
        """   
        connection = await database_connect.get_connection()

        sql_request = f"UPDATE products SET is_active = '{list_of_products.status}' WHERE id = {list_of_products.prod_id[0]}"
        
        if len(list_of_products.prod_id) > 1:
            for i in range (1, len(list_of_products.prod_id)):
                sql_request = sql_request + f" or id = {list_of_products.prod_id[i]}"

        print(sql_request)
        
        await connection.fetch(sql_request)
        await connection.close()


    # Покзывает страницу товара
    async def view_single_product(self, id) -> Product:
        """Возвращает объект Product, если пользователь хочет перейти к конкретному товару
        """   
        connection = await database_connect.get_connection()
        result = await connection.fetch(f"SELECT * FROM products WHERE id = {id}")
        product = Product(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])
        await connection.close()
        return product

products_work_with_db = ProductRepository()

# В ЭТОМ ФАЙЛЕ СОЗДАЕМ БД, ЭТО ДЕЛАЕМ ОДИН РАЗ, НО МОЖЕМ СОЗДАТЬ БД НА ДРУГОМ САЙТЕ, НАПРИМЕР НА БОЕВОМ,ЕГО МЫ В НАЧАЛЕ ЗАПУСТИМ ОТДЕЛЬНО ОТ ВСЕГО ОСТАНОГО
from db.connect_db import database_connect


# Подклоючение к базе
connection = database_connect.get_connection()


# Создаем таблицу - Товары
connection.fetch("""
CREATE TABLE IF NOT EXISTS products (
	id SERIAL PRIMARY KEY,
   	name TEXT NOT NULL,
	price DECIMAL(10, 2) NOT NULL,
	volume DECIMAL(10, 2) NOT NULL,
    color TEXT NOT NULL,
	is_active TEXT NOT NULL
)
""")

# Создаем таблицу - Пользователи
connection.fetch("""
CREATE TABLE IF NOT EXISTS users (
	id SERIAL PRIMARY KEY,
	access TEXT NOT NULL,
   	name TEXT NOT NULL,
	login TEXT NOT NULL,
	password TEXT NOT NULL,
	phone TEXT NOT NULL,
	key TEXT NOT NULL
)
""")

# Создаем таблицу - Заказы
connection.fetch("""
CREATE TABLE IF NOT EXISTS orders (
	id SERIAL PRIMARY KEY,
	status TEXT NOT NULL,
  	phone TEXT NOT NULL,
	user_id INTEGER NOT NULL
)
""")

# Создаем таблицу - Содержимое заказа
connection.fetch("""
CREATE TABLE IF NOT EXISTS products_link_orders (
	id SERIAL PRIMARY KEY,
	order_id INTEGER NOT NULL,
    prod_id INTEGER NOT NULL,
	count DECIMAL(3, 0) NOT NULL
)
""")


# Добавляет к таблице, в данном случае products, новый столбец. Если создавать новую таблицу, нужно удалить старую таблицу и мы потеряем все существующие товары.
# def add_colomn_in_products(self, colomn_name: str):
# 	cursor = database_connect.get_connection()
# 	cursor.execute(f"ALTER TABLE products ADD {colomn_name} INTEGER")
# 	database_connect.connection.commit()


# База данных не может принять запрос, база данных только готовит изменения по запросу, а этот метод  commit() говорит базе данных, что можно вносить измения в базу. При этом все запросы сделаные ранее копятся, т.е сожно сделать много запросов и потом принять один с помощью connection.commit(), это назывется транзакцией.
connection.commit()
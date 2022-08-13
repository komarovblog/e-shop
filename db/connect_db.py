import asyncio
import asyncpg
from asyncpg import Connection
import psycopg2
from psycopg2.extensions import connection


# Асинхронное подключение к БД
class DataBase:
    async def get_connection(self) -> Connection:
        """Асинхронное подключение к БД, для тестов создается синхронное
        """
        return await asyncpg.connect(
                            database ="shop", 
                            user="postgres",
                            password="postgres",
                            host = "localhost",
                            port = "5432")


# Синхронное подключение к БД
class DataBaseNoAsync:
    def get_connection(self) -> connection:
        """Данная функция получает объект Cursor, его можно получить только если есть соединение с БД, если соединение отсутствует, тобиш ошибка, то соединяем снова и получаем Cursor снова. Безопасное получение, устойчивое к обрывам.
        """
        return psycopg2.connect(
                            dbname="shop", 
                            user="postgres",
                            password="postgres",
                            host = "localhost",
                            port = "5432")


database_connect = DataBase()
database_connect_no_async = DataBaseNoAsync()
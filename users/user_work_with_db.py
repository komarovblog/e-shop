# Абсолютный путь начинает из корня проекта и из той же папки из которой буду запускать.
from db.connect_db import database_connect

# Относительный путь иморт из текущий папки, из той в котором текущий файл
from users.user_structure import User

import random
from datetime import date


class UserRepository:

    # Вносит в БД админа
    async def add_user_admin(self, access, name, login, password) -> None:
        """Вносит в БД нового админа
        """   
        connection = await database_connect.get_connection()
        await connection.fetch(f"INSERT INTO users (access, name, login, password) VALUES ({access}, {name}, {login}, {password})")
        # id в базе добавится уникальное автоматически, нужно настроить в БД

        await connection.close()


    # Вносит в БД покупателя
    async def add_user_customer(self, name, phone) -> list:
        """Вносит в БД нового админа и возвращает эту запись из БД
        """ 
        connection = await database_connect.get_connection()
        login = phone

        password_text = "abcTN!z"
        password_list = []
        for i in password_text:
            password_list.append(random.choice(password_text)) 
        password = "".join(password_list)

        new_us = await connection.fetch(f"INSERT INTO users (access, name, login, password, phone, key) VALUES ('customer', '{name}', '{login}', '{password}', '{phone}', 'None') RETURNING id, phone")

        await connection.close()
        return new_us


    # Отправляет пользователю СМС
    def send_sms_for_customer(self) -> None: 
        """Отправляет пользователю СМС
        """
        pass


    # Проверяет ключ пользователя при действиях в админке
    async def check_user_key(self, key) -> int|None:
        """Проверяет ключ пользователя при действиях в админке (редактирование товара, удаление)
        """
        connection = await database_connect.get_connection()
        result = await connection.fetch (f"SELECT id from users WHERE key = '{key}'")

        if len(result) == 0:
            await connection.close()
            return None 

        await connection.close()
        return result[0][0]


    # Проверка доступа при авторизации и перезапись ключа
    async def user_sign_in(self, login, password) -> dict:
        """Проверка доступа при авторизации и перезапись ключа, возвращает запись из БД
        """
        connection = await database_connect.get_connection()
        result = await connection.fetch(f"SELECT login, password, id FROM users WHERE login = '{login}'")

        if result[0][0] is None:
            print("Такой логин не найден")
            return False
       
        if result[0][1] != password:
            print("Пароль не подходит")
            return False

        id = result[0][2]
        date_now = date.today()

        key_text = "abcdefghijklmnopqrstuvwxyz"
        key_list = []

        for symbol in key_text:
            key_list.append(random.choice(key_text))       
        key_part = "".join(key_list)
        key = f"{id}-{date_now}-{key_part}"

        await connection.fetch(f"UPDATE users SET key = '{key}' WHERE login = '{login}'")
        await connection.close()
        return {"key": key, "id": id}


    # Cтирание ключа при выходе
    async def user_sign_out(self, key) -> None:
        """Cтирание ключа при выходе пользователя из системы
        """
        connection = await database_connect.get_connection()
        await connection.fetch(f"UPDATE users SET key = '' WHERE key = '{key}'")
        await connection.close()

      
user_work_with_db = UserRepository()
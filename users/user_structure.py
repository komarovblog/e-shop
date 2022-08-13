from enum import Enum


class AccessEnum(str, Enum):
    """Enum - Класс говорит какие роли могут быть у пользователя
    """    
    admin = "admin"
    customer = "customer"

class User():
    """Класс пользователь (админ и покупатель), за роль отвечает свойство access: AccessEnum
    """
    def __init__(self, id: int, access: AccessEnum, name: str, login: str, password: str, phone: str, key: str):
        self.id = id
        self.access = access
        self.name = name
        self.login = login
        self.password = password
        self.phone = phone
        self.key = key


from enum import Enum
from pydantic import BaseModel


class StatusEnum(str, Enum):
    """Enum - Класс говорит какие статусы могут быть у заказа
    """
    new = "new"
    processing = "processing"
    completed = "completed"

class ProductInOrder(BaseModel):
    """Товар в заказе
    """
    id: int
    name: str
    price: int
    count: int

class Order:
    """Заказ который мы возвращаем пользователю при запросе на просмотр своего заказа
    """
    def __init__(self, id: int, status: StatusEnum, phone: str, user_id: int, prod_in_order: list[ProductInOrder]):
        self.id = id
        self.status = status
        self.phone = phone
        self.user_id = user_id
        self.prod_in_order = prod_in_order

class OrderBaseModel(BaseModel):
    """Заказ который мы возвращаем пользователю при запросе на просмотр своего заказа
    """
    id: int
    status: StatusEnum
    phone: str
    user_id: int
    prod_in_order: list

class IdProduct(BaseModel):
    """Кол-во товара для каждой позиции
    """
    id: str
    count: int

class MakeOrder(BaseModel):
    """Если пользователь делает заказ, то передаем этот обхект в функцию make_order()
    """
    name: str
    phone: str
    list_id_prod: list[IdProduct]

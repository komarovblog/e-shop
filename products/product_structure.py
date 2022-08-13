from enum import Enum
from pydantic import BaseModel

# Класс создает характеристиуку сразу с вариантами, в данном случае цвет (Энкмирация)

class ColorEnum(str, Enum):
    """Enum - Объект содержит данные о возможных цветах товара
    """
    red = "red"
    blue = "blue"
    green = "green"
    black = "black"
    white = "white"

class Product():
    """Объект содержит данные об одном товаре
    """
    def __init__(
                self, 
                id: int, 
                name: str, 
                price: float, 
                volume: float, 
                color: ColorEnum, 
                is_active: str
                ):

        self.id = id
        self.name = name
        self.price = price
        self.volume = volume
        self.color = color
        self.is_active = is_active


class SingleProduct(BaseModel):
    """BaseModel - Объект содержит данные об одном товаре
    """
    name: str = None
    price: float = None
    volume: int = None
    color: ColorEnum = None
    is_active: str = 'Enable'

class Filter(BaseModel):
    """BaseModel - Объект содержит данные для фильтрации, вхождение имени, мин макс цены, номер страниы и кол-во товаров на странице
    """
    name: str = None
    price_min: int = None 
    price_max: int = None 
    page_number: int = 1
    prod_on_page: int = 7

class ListNewProducts(BaseModel):
    name: str
    price: float
    volume: int
    color: ColorEnum

class ResultAfterGetProduct(BaseModel):
    products: list
    count_page: int

class EnableDisableProd(BaseModel):
    prod_id: list[int] = []
    status: str = None
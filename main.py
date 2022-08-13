# https://fastapi.tiangolo.com/tutorial/query-params/

from fastapi import Request
from fastapi import FastAPI, Header, APIRouter

from products.product_structure import Product, SingleProduct, Filter, ResultAfterGetProduct,EnableDisableProd
from products.products_work_with_db import products_work_with_db

from users.user_structure import User
from users.user_work_with_db import user_work_with_db

from orders.order_structure import Order, IdProduct
from orders.order_work_with_db import order_work_with_db
from orders.order_structure import MakeOrder

# Чтобы выкинуть исключение
from fastapi.exceptions import HTTPException

app = FastAPI()
router = APIRouter()

# 01. ПРОДУКТЫ

# Фильтрация товаров 
@router.get("/products") 
async def filter_products_api(    
                                name: str = None,
                                price_min: int = None ,
                                price_max: int = None 
                                                        ) -> ResultAfterGetProduct:
    filter = Filter(name = name, price_min = price_min, price_max = price_max)
    prod_list = await products_work_with_db.get_products(filter = filter)
    prod_list_conv = products_work_with_db.convert_products_in_list_object(prod_list)
    count_page = products_work_with_db.make_pagination(filter, prod_list_conv)
    result = ResultAfterGetProduct(products = prod_list_conv, count_page = count_page)
    return result

# Детальная товара
@router.get("/products/{id}")
async def view_single_product_api(id: str) -> Product:
    return await products_work_with_db.view_single_product(id)


# 02. ПОЛЬЗОВАТЕЛИ

# Авторизация
@router.post("/sign_in") 
async def user_sign_in_api(login: str = Header(None), password: str = Header(None)) -> dict:
    if login is None:
        return {"key": False}
    result = await user_work_with_db.user_sign_in(login, password)
    if result == False:
       raise HTTPException(403) # Выбрасываем ошибку 
    
    return {"key": result["key"], "id": result["id"]}

# Добавление товара 
@router.post("/admin/add_products")
async def insert_product_api(list_new_products: list[SingleProduct], key = Header()) -> bool: 
    if await user_work_with_db.check_user_key(key):
        await products_work_with_db.insert_product(list_new_products)
        return True
    return False

# Редактирование товара
@router.put("/admin/edit_product/{prod_id}")
async def edit_product_api(prod_id: int, new_params: SingleProduct, key = Header()) -> bool: 
    if await user_work_with_db.check_user_key(key):
        if await products_work_with_db.edit_product(prod_id, new_params):
            return True
    return False

# Включение, выключение товаров
@router.put("/admin/products")
async def enable_disable_product_api(list_prod: EnableDisableProd, key = Header()) -> bool: 
    if await user_work_with_db.check_user_key(key):
        if list_prod.status != None and len(list_prod.prod_id) > 0:
            await products_work_with_db.enable_disable_product(list_prod)
        return True
    return False

# Выйти из системы, стирание ключа
@router.post("/sign_out")
async def user_sign_out_api(key: str | None = Header()) -> bool:
    if key is None:
        print("if key is None:")
        return False
    if await user_work_with_db.check_user_key(key):
        print("if await user_work_with_db.check_user_key(key)")
        await user_work_with_db.user_sign_out(key)
        return True
    print("END")
    return False


# 03. ЗАКАЗЫ

# Сделать заказ 
@router.post("/order")
async def make_order_api(data_order: MakeOrder):
    order_id = await order_work_with_db.make_order(data_order)   
    user_work_with_db.send_sms_for_customer()
    return order_id

# Посмотреть все заказы пользователя
@router.get("/order/all")
async def view_all_orders_api(key = Header()) -> list:
    user_id = await user_work_with_db.check_user_key(key)
    if user_id is not None:
        return await order_work_with_db.show_all_orders(user_id)
    raise HTTPException(403) # Выбрасываем ошибку

# Посмотреть заказ
@router.get("/order/{order_id}")
async def view_order_api(order_id, key = Header()) -> list[Order]:
    if await user_work_with_db.check_user_key(key):
        return await order_work_with_db.show_order(order_id)
    return False


################################################################

@router.get("/query")
def testim_api(req: Request):
    # print(req.)
    print(req.headers)
    print(req.query_params)

app.include_router(router, prefix="/api")

################################################################

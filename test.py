from fastapi.testclient import TestClient
from main import app
from db.connect_db import database_connect

from tests.test_products import test_products
from tests.test_users import test_users
from tests.test_orders import test_orders

# В зависимости от теструемого раздела, раскоментируем одну из строк ниже.
# test_products()
# test_users()
# test_orders()
# test_order_sync()
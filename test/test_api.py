import pytest
import allure
from api.get_product_api import GetProduct
from configuration.ConfigProvider import ConfigProvider
from configuration.DataApiProvider import Data_ApiProvider
from api.basket import Basket


@pytest.mark.api
@allure.story("Проверка поля поиска")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный тест проверки нахождения товара ")
@allure.description("""Проверяет успешный поиск товара
                    с указанным валидным названием.""")
@pytest.mark.parametrize('locator', range(0, len(Data_ApiProvider().data['positiv_search_data'])))
def positiv_get_test(locator):
    with allure.step("Подготовка данных"):
        bas_url = ConfigProvider().get('api', 'bas_url_v2')
        product_name = Data_ApiProvider().data['positiv_search_data'][locator]['product_name']
        location = '77000000000000000000000000'
    with allure.step(f"Отправляем запрос на поиск товара '{product_name}'"):
        getProduct = GetProduct(bas_url, product_name, location)
        resp = getProduct.get_pruduct()
    with allure.step(f"Анализируем полученный ответ ({resp.status_code})"):
        assert resp.status_code == 200, f'Неверный статус код {resp.status_code}'
        data: dict = resp.json()
        items = data.get('success_response', {}).get('items', [])
        assert isinstance(items, list), "Список товаров ('items') не найден или не является списком"
    with allure.step(f"Ищем продукты, соответствующие названию '{product_name}'"):
        product_items = [item for item in items if product_name in item.get('name', '')]
        assert len(product_items) > 0, f"Ни один товар с именем {product_name} не найден!"


@pytest.mark.api
@allure.story("Проверка поля поиска")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Негативный тест проверки нахождения товара ")
@allure.description("""Проверяет неуспешный поиск товара
                    с указанным невалидным названием.""")
@pytest.mark.parametrize('locator', range(0, len(Data_ApiProvider().data['negativ_search_data'])))
def negativ_get_test(locator):
    with allure.step("Подготовка данных"):
        bas_url_v2 = ConfigProvider().get('api', 'bas_url_v2')
        product_name = Data_ApiProvider().data['negativ_search_data'][locator]['product_name']
        location = '77000000000000000000000000'
    with allure.step(f"Отправляем запрос на поиск товара '{product_name}'"):
        getProduct = GetProduct(bas_url_v2, product_name, location)
        resp = getProduct.get_pruduct()
        statuc_code = resp.json()["error_backend"]["error_backend_autocomplete"]["http_status_code"]
    with allure.step(f"Анализируем полученный ответ ({statuc_code})"):
        assert getProduct.get_pruduct().status_code == 200
        assert resp.json()["error_backend"]["error_backend_autocomplete"]["http_status_code"] == 406


@pytest.mark.api
@allure.story("Проверка корзины")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тестирование корзины")
@allure.description("""Положить товар в корзину, удалить товар из корзины.""")
def basket_test():
    with allure.step("Подготовка данных"):
        bas_url_v1 = ConfigProvider().get('api', 'bas_url_v1')
        bas_url = ConfigProvider().get('api', 'bas_url_v2')
        product_name = Data_ApiProvider().data['positiv_search_data'][0]['product_name']
        location = '77000000000000000000000000'
    with allure.step(f"Отправляем запрос на поиск товара '{product_name}'"):
        getProduct = GetProduct(bas_url, product_name, location)
        resp = getProduct.get_pruduct()
        id_res = resp.json()["success_response"]["items"][0]["id"]
    with allure.step(f"Анализируем полученный ответ ({resp.status_code})"):
        assert resp.status_code == 200, f'Неверный статус код {resp.status_code}'
        put_Product = Basket(bas_url_v1, id_res)
    with allure.step("Положить товар в корзину"):
        put_resp = put_Product.put_pruduct()
        assert put_resp.json()["personalCart"]["items"][0]["cartItemId"] > 0
        cartItemId = put_resp.json()["personalCart"]["items"][0]["cartItemId"]
    with allure.step(f"Номер товара в корзине {cartItemId}"):
        pass
    with allure.step(f"Анализируем полученный ответ ({put_resp.status_code})"):
        assert put_resp.status_code == 200, f"Полученный статус код {put_resp.status_code}"
        assert put_resp.json()["personalCart"]["items"][0]["id"] == int(id_res)
    with allure.step(f"Номер товара  {put_resp.json()["personalCart"]["items"][0]["id"]}"):
        pass
    with allure.step("Удалить товар из корзины"):
        del_resp = put_Product.del_product(cartItemId)
        assert del_resp.status_code == 200, f"Полученный статус код {del_resp.status_code}"
        assert len(del_resp.json()["items"]) == 0, "Корзина не пустая"
    with allure.step("Корзина пустая"):
        pass


@pytest.mark.api
@allure.story("Проверка корзины")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Изменение количества товара в корзине")
@allure.description("""Положить товар в корзину,
                    изменить количество,
                     удалить товар из корзины.""")
def patch_basket_test():
    with allure.step("Подготовка данных"):
        bas_url_v1 = ConfigProvider().get('api', 'bas_url_v1')
        bas_url = ConfigProvider().get('api', 'bas_url_v2')
        product_name = Data_ApiProvider().data['positiv_search_data'][0]['product_name']
        location = '77000000000000000000000000'
    with allure.step(f"Отправляем запрос на поиск товара '{product_name}'"):
        getProduct = GetProduct(bas_url, product_name, location)
        resp = getProduct.get_pruduct()
        id_res = resp.json()["success_response"]["items"][0]["id"]
    with allure.step(f"Анализируем полученный ответ ({resp.status_code})"):
        assert resp.status_code == 200, f'Неверный статус код {resp.status_code}'
        put_Product = Basket(bas_url_v1, id_res)
    with allure.step("Положить товар в корзину"):
        put_resp = put_Product.put_pruduct()
        assert put_resp.json()["personalCart"]["items"][0]["cartItemId"] > 0
        cartItemId = put_resp.json()["personalCart"]["items"][0]["cartItemId"]
    with allure.step(f"Анализируем полученный ответ ({put_resp.status_code})"):
        assert put_resp.status_code == 200, f"Полученный статус код {put_resp.status_code}"
        assert put_resp.json()["personalCart"]["items"][0]["id"] == int(id_res)
    with allure.step(f"Номер товара  {put_resp.json()["personalCart"]["items"][0]["id"]}"):
        pass
    with allure.step(f"Номер товара в корзине {cartItemId}"):
        pass
    quantity = put_resp.json()["personalCart"]["items"][0]["quantity"]
    with allure.step(f"Количество товара в корзине {quantity}"):
        pass
    with allure.step("Меняем количество товара на 10"):
        quantity = 10
    patch_resp = put_Product.patch_product(quantity)
    patch_resp.json()["items"][0]["quantity"]
    with allure.step(f"Анализируем полученный ответ ({patch_resp.status_code})"):
        assert put_resp.status_code == 200, f"Полученный статус код {patch_resp.status_code}"
    assert patch_resp.json()["items"][0]["quantity"] == 10
    with allure.step(f"Количество товара изменено на {patch_resp.json()["items"][0]["quantity"]}"):
        pass
    with allure.step("Удалить товар из корзины"):
        del_resp = put_Product.del_product(cartItemId)
        assert del_resp.status_code == 200, f"Полученный статус код {del_resp.status_code}"
        assert len(del_resp.json()["items"]) == 0, "Корзина не пустая"
    with allure.step("Корзина пустая"):
        pass


@pytest.mark.api
@allure.story("Проверка корзины")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Повторное удаление удаленного товара из корзины")
@allure.description("""Положить товар в корзину, удалить товар из корзины.""")
def del_basket_test():
    with allure.step("Подготовка данных"):
        bas_url_v1 = ConfigProvider().get('api', 'bas_url_v1')
        bas_url = ConfigProvider().get('api', 'bas_url_v2')
        product_name = Data_ApiProvider().data['positiv_search_data'][0]['product_name']
        location = '77000000000000000000000000'
    with allure.step(f"Отправляем запрос на поиск товара '{product_name}'"):
        getProduct = GetProduct(bas_url, product_name, location)
        resp = getProduct.get_pruduct()
        id_res = resp.json()["success_response"]["items"][0]["id"]
    with allure.step(f"Анализируем полученный ответ ({resp.status_code})"):
        assert resp.status_code == 200, f'Неверный статус код {resp.status_code}'
        put_Product = Basket(bas_url_v1, id_res)
    with allure.step("Положить товар в корзину"):
        put_resp = put_Product.put_pruduct()
        assert put_resp.json()["personalCart"]["items"][0]["cartItemId"] > 0
        cartItemId = put_resp.json()["personalCart"]["items"][0]["cartItemId"]
    with allure.step(f"Номер товара в корзине {cartItemId}"):
        pass
    with allure.step(f"Анализируем полученный ответ ({put_resp.status_code})"):
        assert put_resp.status_code == 200, f"""Полученный статус код {put_resp.status_code}"""
        assert put_resp.json()["personalCart"]["items"][0]["id"] == int(id_res)
    with allure.step(f"Номер товара  {put_resp.json()["personalCart"]["items"][0]["id"]}"):
        pass
    with allure.step("Удалить товар из корзины"):
        del_resp = put_Product.del_product(cartItemId)
        assert del_resp.status_code == 200, f"Полученный статус код {del_resp.status_code}"
        assert len(del_resp.json()["items"]) == 0, "Корзина не пустая"
    with allure.step("Корзина пустая"):
        pass
    with allure.step("Повторное удаление товара из корзины"):
        del_resp = put_Product.del_product(cartItemId)
        assert del_resp.status_code == 400, f"""
        Полученный статус код {del_resp.status_code}"""
        assert len(del_resp.json()["items"]) == 0, "Корзина не пустая"
    with allure.step("Корзина пустая"):
        pass

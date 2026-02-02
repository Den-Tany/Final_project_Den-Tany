import allure
import pytest
from configuration.ConfigProvider import ConfigProvider
from page.MainePage import MainePage
from configuration.DataProvider import DataProvider
from selenium.webdriver.common.by import By


@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Проверка работоспособности кнопки")
@allure.title("""Перход по кнопке""")
@allure.description("""При нажатии на кнопку происходит переход на страницу""")
@pytest.mark.parametrize('locator', range(0, len(DataProvider().data['button_nav'])))
def button_click_test(browser, web, locator):
    with allure.step("Подготовка данных"):
        button_name = DataProvider().data['button_nav'][locator]['button_name']
        button_locator = f"{DataProvider().data['button_nav'][locator]['xpath_locator']}'{button_name}')]"
        button_url = DataProvider().data['button_nav'][locator]['expected_url']
        maine_page = MainePage(browser, locator, button_locator, button_name)
    # Поиск элемента на странице по локатору и названию
    assert maine_page.find_elem(), f"""Кнопка по заданному
                локатору с названием
            <{button_name}> не существует"""
    with allure.step(f"""Кнопка по заданному
                локатору с названием
            <{button_name}> существует"""):
        pass
    # Проверка активности элемента
    assert maine_page.elem_clickable(), f"""Кнопка по заданному
                локатору с названием
                <{button_name}> неактивна"""
    with allure.step(f"""Кнопка по заданному
                локатору с названием
                <{button_name}> активна"""):
        pass
    # Кликаем на элемент и проверяем правильность перехода
    get_url = maine_page.button_click()
    expected_url = f"{ConfigProvider().get('ui', 'bas_url')}{button_url}"
    assert get_url == expected_url, f"Переход не произошел на страницу: {get_url}"
    with allure.step(f"Переход произошел на страницу: {get_url}"):
        pass


@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Проверка поля поиска")
@allure.title("""Позитивный тест поля поиска товара""")
@allure.description("""Проверяется что поле существует,
                    активно для работы.
                    После ввода и поиска товароа считает общее количество
                    товара в названии которого присутствует искомое название.""")
@pytest.mark.parametrize('locator', range(0, len(DataProvider().data['positiv_search_data'])))
def positiv_search_field_test(browser, web, locator):
    # Запрашиваем данные из файла data1.json для поля поиска
    with allure.step("Подготовка данных"):
        field_name = DataProvider().data['search_field'][0]['field_name']
        field_locator = f"{DataProvider().data['search_field'][0]['xpath_locator']}'{field_name}']"
    maine_page = MainePage(browser, locator, field_locator, field_name)
    # Определяем, что поле поиска существует
    assert maine_page.find_elem(), "Поле не найдено"
    with allure.step("Поле найдено"):
        pass
    # Определяем, что поле активно и доступно
    assert maine_page.elem_clickable(), "Поле не активно"
    with allure.step("Поле активно"):
        pass
    # Кликаем на поле ввода, открывается страница поиска товара
    maine_page.button_click()
    # Запрашиваем данные из файла data1.json для поля ввода
    with allure.step("Подготовка данных. Запрашиваем что искать."):
        field_name = 'Поле ввода'
        field_locator = "//input[@id='search-popup-field']"
        # Запрашиваем что искать из файла data1.json
        product_name = DataProvider().data['positiv_search_data'][locator]['product_name']
        maine_page = MainePage(browser, locator, field_locator, field_name)
    # Определяем, что поле поиска существует
    assert maine_page.find_elem(), "Поле не найдено"
    with allure.step("Поле найдено"):
        pass
    # Определяем, что поле активно и доступно
    assert maine_page.elem_clickable(), "Поле не активно"
    with allure.step("Поле активно"):
        pass
    # Вводим в поле данные для поиска
    maine_page.input_value(product_name)
    total_count = maine_page.request_processing(product_name)
    # with allure.step(f"Количесто товаров, содержащие в названии <{product_name}>"):
    assert total_count > 0, f"Товар содержащий в названии <{product_name}> не найден."
    with allure.step(f"Общее количество товаров, содержащий <{product_name}> равно <{total_count}>"):
        pass


@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Проверка поля поиска")
@allure.title("""Негативный тест поля поиска товара""")
@allure.description("""Проверяется что поле существует,
                    активно для работы.
                    После ввода негативного значения
                    поле результатов должно быть пустым.""")
@pytest.mark.parametrize('locator', range(0, len(DataProvider().data['negativ_search_data'])))
def negativ_search_field_test(browser, web, locator):
    with allure.step("Подготовка данных"):
        # Запрашиваем данные из файла data1.json для поля поиска
        field_name = DataProvider().data['search_field'][0]['field_name']
        field_locator = f"{DataProvider().data['search_field'][0]['xpath_locator']}'{field_name}']"
    maine_page = MainePage(browser, locator, field_locator, field_name)
    # Определяем, что поле поиска существует
    assert maine_page.find_elem(), "Поле не найдено"
    with allure.step("Поле найдено"):
        pass
    # Определяем, что поле активно и доступно
    assert maine_page.elem_clickable(), "Поле не активно"
    with allure.step("Поле активно"):
        pass
    # Кликаем на поле ввода, открывается страница поиска товара
    maine_page.button_click()
    with allure.step("Подготовка данных. Запрашиваем что искать."):
        # Запрашиваем данные из файла data1.json для поля ввода
        field_name = DataProvider().data['search_field_v2'][0]['field_name']
        field_locator = DataProvider().data['search_field_v2'][0]['xpath_locator']
        # Запрашиваем что искать из файла data1.json
        product_name = DataProvider().data['negativ_search_data'][locator]['product_name']
    maine_page = MainePage(browser, locator, field_locator, field_name)
    # Определяем, что поле поиска существует
    assert maine_page.find_elem(), "Поле не найдено"
    with allure.step("Поле найдено"):
        pass
    # Определяем, что поле активно и доступно
    assert maine_page.elem_clickable(), "Поле не активно"
    with allure.step("Поле активно"):
        pass
    # Вводим в поле данные для поиска
    maine_page.input_value(product_name)
    total_count = maine_page.request_processing(product_name)
    assert total_count == 0, f"Товар содержащий в названии <{product_name}> не должен был быть найден."
    with allure.step(f"Общее количество товаров, содержащий <{product_name}> равно <{total_count}>"):
        pass


@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Корзина")
@allure.title("""Положить товар в корзину""")
@allure.description("""После загрузки сайта выбираем первый товар из предложенного списка.
        Нажимает кнопку "Купить".
        В открывшемся окне нажимаем кнопку "В корзину".
        В открывшемся окне "Корзина" проверяем, что она не пуста.
        Нажимаем на кнопку "Удалить" (Пиктограмма мусорного бачка).
        Проверяем, что корзина пуста.
        """)
def basket_test(browser, web):
    with allure.step('Выбрать товар и нажать кнопку "Купить"'):
        # Загружаем данные кнопки "Купить" и кликаем на неё
        locator = 0
        button_name = DataProvider().data['basket'][0]['button_name']
        button_locator = DataProvider().data['basket'][0]['xpath_locator']
        maine_page = MainePage(browser, locator, button_locator, button_name)
        maine_page.scroll_elem()
        assert maine_page.find_elem(), f"""Кнопка по заданному
                локатору с названием
            <{button_name}> не существует"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                <{button_name}> существует"""):
            pass
        assert maine_page.elem_clickable(), f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> неактивна"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> активна"""):
            pass
    get_url = maine_page.button_click()
    with allure.step('Нажать кнопку "В корзину"'):
        # Загружаем данные кнопки "В корзину" и кликаем на неё
        locator = 0
        button_name = DataProvider().data['basket'][1]['button_name']
        button_locator = DataProvider().data['basket'][1]['xpath_locator']
        button_url = DataProvider().data['basket'][1]['expected_url']
        maine_page = MainePage(browser, locator, button_locator, button_name)
        assert maine_page.find_elem(), f"""Кнопка по заданному
                локатору с названием
            <{button_name}> не существует"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                <{button_name}> существует"""):
            pass
        assert maine_page.elem_clickable(), f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> неактивна"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> активна"""):
            pass
    get_url = maine_page.button_click()
    expected_url = f"{ConfigProvider().get('ui', 'bas_url')}{button_url}"
    assert get_url == expected_url, f"Переход не произошел на страницу: {get_url}"
    with allure.step(f"Переход произошел на страницу: {get_url}"):
        pass
    assert len(browser.find_elements(By.CLASS_NAME, 'basket-structure__list')) > 0, "Корзина пустая"
    with allure.step("Корзина не пустая"):
        pass
    with allure.step('Нажать кнопку "Удалить"'):
        # Загружаем данные кнопки "Удалить" и кликаем на неё
        locator = 0
        button_name = DataProvider().data['basket'][3]['button_name']
        button_locator = DataProvider().data['basket'][3]['xpath_locator']
        maine_page = MainePage(browser, locator, button_locator, button_name)
        assert maine_page.find_elem(), f"""Кнопка по заданному
                локатору с названием
            <{button_name}> не существует"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                <{button_name}> существует"""):
            pass
        assert maine_page.elem_clickable(), f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> неактивна"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> активна"""):
            maine_page.button_click()
            pass
        assert len(browser.find_elements(By.CLASS_NAME, 'basket-structure__list')) == 0, "Корзина не пустая"
        with allure.step("Корзина пустая"):
            pass


@pytest.mark.ui
@allure.severity(allure.severity_level.CRITICAL)
@allure.story("Корзина")
@allure.title("""Уменьшить количество товара в корзине""")
@allure.description("""После загрузки сайта выбираем первый товар из предложенного списка.
        Нажимает кнопку "Купить".
        В открывшемся окне нажимаем кнопку "В корзину".
        В открывшемся окне "Корзина" проверяем, что она не пуста.
        В "Корзине" вабранный товар в количестве 1 шт пытаемся уменьшить на 1.
        Нажимаем на кнопку "Удалить" (Пиктограмма мусорного бачка).
        Проверяем, что корзина пуста.
        """)
def negativ_patch_basket_test(browser, web):
    with allure.step('Выбрать товар и нажать кнопку "Купить"'):
        # Загружаем данные кнопки "Купить" и кликаем на неё
        locator = 0
        button_name = DataProvider().data['basket'][0]['button_name']
        button_locator = DataProvider().data['basket'][0]['xpath_locator']
        maine_page = MainePage(browser, locator, button_locator, button_name)
        maine_page.scroll_elem()
        assert maine_page.find_elem(), f"""Кнопка по заданному
                локатору с названием
            <{button_name}> не существует"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                <{button_name}> существует"""):
            pass
        assert maine_page.elem_clickable(), f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> неактивна"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> активна"""):
            pass
    get_url = maine_page.button_click()
    with allure.step('Нажать кнопку "В корзину"'):
        # Загружаем данные кнопки "В корзину" и кликаем на неё
        locator = 0
        button_name = DataProvider().data['basket'][1]['button_name']
        button_locator = DataProvider().data['basket'][1]['xpath_locator']
        button_url = DataProvider().data['basket'][1]['expected_url']
        maine_page = MainePage(browser, locator, button_locator, button_name)
        assert maine_page.find_elem(), f"""Кнопка по заданному
                локатору с названием
            <{button_name}> не существует"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                <{button_name}> существует"""):
            pass
        assert maine_page.elem_clickable(), f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> неактивна"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> активна"""):
            pass
    get_url = maine_page.button_click()
    expected_url = f"{ConfigProvider().get('ui', 'bas_url')}{button_url}"
    assert get_url == expected_url, f"Переход не произошел на страницу: {get_url}"
    with allure.step(f"Переход произошел на страницу: {get_url}"):
        pass
    assert len(browser.find_elements(By.CLASS_NAME, 'basket-structure__list')) > 0, "Корзина пустая"
    with allure.step("Корзина не пустая"):
        pass
    # Загружаем данные кнопки "Минус" и кликаем на неё
    locator = 0
    button_name1 = DataProvider().data['basket'][2]['button_name']
    button_locator = DataProvider().data['basket'][2]['xpath_locator']
    maine_page = MainePage(browser, locator, button_locator, button_name1)
    assert maine_page.find_elem(), f"""Кнопка по заданному
            локатору с названием
        <{button_name}> не существует"""
    with allure.step(f"""Кнопка по заданному
                локатору с названием
            <{button_name}> существует"""):
        pass
    Clik = maine_page.elem_clickable()

    with allure.step('Нажать кнопку "Удалить"'):
        # Загружаем данные кнопки "Удалить" и кликаем на неё
        locator = 0
        button_name = DataProvider().data['basket'][3]['button_name']
        button_locator = DataProvider().data['basket'][3]['xpath_locator']
        maine_page = MainePage(browser, locator, button_locator, button_name)
        assert maine_page.find_elem(), f"""Кнопка по заданному
                локатору с названием
            <{button_name}> не существует"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                <{button_name}> существует"""):
            pass
        assert maine_page.elem_clickable(), f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> неактивна"""
        with allure.step(f"""Кнопка по заданному
                    локатору с названием
                    <{button_name}> активна"""):
            maine_page.button_click()
            pass
        assert len(browser.find_elements(By.CLASS_NAME, 'basket-structure__list')) == 0, "Корзина не пустая"
        with allure.step("Корзина пустая"):
            pass

    try:
        if not Clik:
            with allure.step(f"Кнопка по заданному локатору с названием '{button_name1}' не активна"):
                pass
        else:
            with allure.step(f"Кнопка по заданному локатору с названием '{button_name1}' активна"):
                pytest.fail("Тест не пройден: кнопка активна")
    except AssertionError as e:
        with allure.step(str(e)):
            pytest.fail("Тест не пройден: проблема с кликабельностью кнопки")

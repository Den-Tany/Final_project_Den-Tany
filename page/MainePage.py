# MainePage.py
import allure
import pytest
from configuration.ConfigProvider import ConfigProvider
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys


class MainePage:

    def __init__(self, driver: WebDriver, locator: int, locator_elem: str, elem_name: str):
        self.driver = driver
        self.locator_elem = locator_elem
        self.elem_name = elem_name
        self.locator = locator
        self.element = None

    def scroll_elem(self):
        """
        Прокручиваем страницу до элемента
        """
        self.driver.implicitly_wait(10)
        element = self.driver.find_element(By.XPATH, self.locator_elem)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.driver.implicitly_wait(10)

    def find_elem(self):
        """
        Поиск элемента по локатору
        """
        try:
            with allure.step(f"Найти элемент <{self.elem_name}>"):
                self.element = WebDriverWait(self.driver, ConfigProvider().getint('ui', 'timeout')).until(EC.visibility_of_element_located((By.XPATH, self.locator_elem)))
                return True
        except (NoSuchElementException, TimeoutException):
            return False

    def elem_clickable(self):
        """
        Проверка кликабельности найденого элемента
        """
        try:
            with allure.step(f"Проверка кликабельности элемента '{self.elem_name}'"):
                enabled = self.element.is_enabled()
                displayed = self.element.is_displayed()
                if enabled and displayed:
                    return True
        except NoSuchElementException:
            return False

    def button_click(self):
        """
        Клик на элемент
        """
        with allure.step(f"Кликнуть на элемент '{self.elem_name}'"):
            try:
                self.element.click()
                self.driver.implicitly_wait(
                    ConfigProvider().getint('ui', 'timeout'))
                """"
                Загружает в переменную текущий URL адрес
                """
                current_url = self.driver.current_url
                return current_url
            except ElementClickInterceptedException:
                pytest.fail("Кнопка закрыта другим элементом")
                return None

    def input_value(self, product_name):
        """"
        Ввод значения для поиска
        """
        self.driver.implicitly_wait(
                ConfigProvider().getint('ui', 'timeout'))
        # Очистить поле
        self.element.clear()
        # Ввод значения
        self.element.send_keys(product_name)
        # нажать кнопку ENTER
        self.element.send_keys(Keys.ENTER)

    def request_processing(self, product_name):
        try:
            # Сначала ждем появления блока, сигнализирующего о результатах поиска
            WebDriverWait(self.driver, ConfigProvider().getint('ui', 'timeout')).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.search-no-results-block__content'))
            )
            # Если блок появился, значит результатов нет
            return 0  # Или любое другое значение, означающее отсутствие результата
        except TimeoutException:
            pass  # Блок не появился, идём дальше искать элементы товаров
        try:
            # Теперь ищем карточки продуктов
            child_containers = WebDriverWait(self.driver, ConfigProvider().getint('ui', 'timeout')).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.product-card__rating-and-name-block'))
            )
            # Подсчет карточек, содержащих указанное название продукта
            containers_with_product_name = sum(product_name.lower() in container.text.lower() for container in child_containers)
            return containers_with_product_name
        except NoSuchElementException:
            return 0  # Элементы не найдены
        except Exception as ex:
            print(f"Ошибка при обработке запроса: {ex}")
            return 0

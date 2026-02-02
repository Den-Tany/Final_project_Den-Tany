import allure
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from configuration.ConfigProvider import ConfigProvider
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


@allure.title("Работа выбранного драйвера браузера")
@pytest.fixture(scope='session')
def browser():
    """
    Загрузка выбранного драйвера браузера Chrom или Firefox.
    Открытие браузера.
    По окончании теста - закрытие браузера.
    """
    browser_name = ConfigProvider().config.get('ui', 'browser_name')
    driver = None
    if (browser_name == 'chrom'):
        with allure.step("""Загрузка драйвера браузера Chrom"""):
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    else:
        with allure.step("""Загрузка драйвера браузера Firefox"""):
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    # Ожидание после открытия браузера
    driver.implicitly_wait(ConfigProvider().getint('ui', 'timeout'))
    # Раскрытие окна в максимальный размер
    with allure.step("Открытие браузера"):
        driver.maximize_window()
    yield driver
    with allure.step("Закрытие браузера"):
        driver.quit()


@allure.title("Переход на тестируемый сайт")
@pytest.fixture
def web(browser: WebDriver):
    """
    Переход на тестируемый сайт
    """
    with allure.step(f"""Загрузка тестируемого сайта
                     {ConfigProvider().get('ui', 'bas_url')}"""):
        browser.implicitly_wait(ConfigProvider().getint('ui', 'timeout'))
        browser.get(ConfigProvider().get('ui', 'bas_url'))
    try:
        # Ожидание появления элемента регион'
        element = WebDriverWait(browser, 4).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.confirm-region")))
        # Поиск кнопки закрыть
        button = element.find_element(By.CSS_SELECTOR, "button.mtsds-button.confirm-region__close")
        # Нажатие на кнопку
        button.click()
    except ElementNotInteractableException:
        pass
    try:
        # Ждем появление алерта
        alert = WebDriverWait(browser, 4).until(EC.alert_is_present())
        # Блокирование .dismiss() или .accept(), если нужно подтвердить алерт
        alert.dismiss()
    except TimeoutException:
        pass  # Алерта нет, продолжаем выполнение теста

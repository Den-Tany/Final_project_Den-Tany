# Автоматизирование UI- и API-тестов.
## Тестирование сайта https://shop.mts.ru
## Задачи реализованные в проекте.
### UI тестирование
<ol>
<li>Тестирование работоспособности кнопок: кликабельность, правильность перехода.</li>
<li>Тестирование "Поле поиска товара": правильность обработки валидных и невалидных запросов.</li>
<li>Тестирование корзины.</li>
<ol>
<li> Добавление товара в корзину</li>
<li> Удаление товара из корзины</li>
<li> Тестирование возможности уменьшения количества товара в корзине, если количество товара равно 1 шт</li>
</ol>
</ol>

### API тестирование
<ol>
<li>Составление GET запросов на вызов списка товаров по валидным и невалидным значениям.</li>
<li>Составление POST запроса на добавление товара в корзину.</li>
<li>Составление DELETE запросов на удаление из корзины товаров.</li>
<li>Составление PATCH запросов на изменение количества товара в корзине.</li>
</ol>

#### [Cылка](https://dem-7.yonote.ru/share/b9b9dd4d-b1fa-4bcc-979d-2a2798e1ad95) на финальный проект по ручному тестированию
### Шаги
1. Клонировать git репозиторий 'https://github.com/Den-Tany/Final_project_Den-Tany.git'
2. Установить зависимости 'python -m pip install -r requirements.txt'
3. Запустить тесты:
- Запустить ui тесты: 'pytest -m "ui" --alluredir allure-results'
- Запустить api тесты: 'pytest -m "api" --alluredir allure-results'
- Запустить все тесты: 'pytest --alluredir allure-results'
4. Сгенерировать и открыть отчет: 'allure serve allure-results'

### Стек - 
- pytest
- selenium
- requests
- allure
- configparser
- json
- webdrivermanager

### Структура
- ./testdata - _папка с данными для тестирования
- ./test - _папка с тестами_
- ./page - _папка с функциями для ui тестирования_
- ./configuration - _папка конфигурирования данных_
- ./api - _папка с функциями для api тестирования_
- config.ini - файл настройки тестов
- pytest.ini - файл настройки параметров тестирования

### Полезные ссылки
- [Гайд по Markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла gitignore](https://www.toptal.com/developers/gitignore/)
- [Про pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/)



# DataProvider.py
import json

my_file = open('testdata/data_ui.json', 'r', encoding='utf-8')
global_data = json.load(my_file)


class DataProvider:
    """
    Создает переменную куда записываются
     данные из файла data.json
    """
    def __init__(self):
        self.data: dict = global_data

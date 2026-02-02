import json

my_file = open('testdata/data_api.json', 'r', encoding='utf-8')
global_data = json.load(my_file)


class Data_ApiProvider:
    """
    Создает переменную куда записываются
     данные из файла data_api.json
    """
    def __init__(self):
        self.data: dict = global_data

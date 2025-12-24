# ConfigPrivider.py
import configparser

global_config = configparser.ConfigParser()
global_config.read('config.ini')


class ConfigProvider:
    """
    Создает переменную с данными из файла config.ini
    """
    def __init__(self):
        self.config = global_config

    def get(self, section: str, prop: str):
        """"
        Возвращает строковое значение переменной из файла config.ini
        """
        return self.config[section].get(prop)

    def getint(self, section: str, prop: int):
        """"
        Возвращает целочисленное значение переменной из файла config.ini
        """
        return self.config[section].getint(prop)

    def getboolean(self, section: str, prop: bool):
        """"
        Возвращает булевое значение переменной из файла config.ini
        """
        return self.config[section].getboolean(prop)

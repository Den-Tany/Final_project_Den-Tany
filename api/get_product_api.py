import requests


class GetProduct:
    def __init__(self, bas_url, product_name, location):
        self.bas_url = bas_url
        self.product_name = product_name
        self.location = location

    def get_pruduct(self):
        path1 = "v2/search/products?st="
        path2 = "&showUnavailable=true&location="
        res = requests.get(f'{self.bas_url}{path1}{self.product_name}{path2}{self.location}')
        return res

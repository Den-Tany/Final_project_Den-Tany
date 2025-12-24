import requests


class Basket:
    def __init__(self, bas_url, id_res):
        self.bas_url = bas_url
        self.id_res = id_res

    def put_pruduct(self):
        res = requests.post(f'{self.bas_url}v1/cart/add', json={"id": self.id_res, "quantity": 1})
        return res

    def patch_product(self, quantity):
        res = requests.patch(f'{self.bas_url}v1/baskets/current/items', json={"products": [{"quantity": quantity, "id": self.id_res}], "corporate": True})
        return res

    def get_pruduct(self):
        res = requests.get('https://shop.mts.ru/api/v1/baskets/current?corporate=false')
        return res

    def del_product(self, cartItemId: int):
        res = requests.delete(f'{self.bas_url}v1/baskets/current/items/{cartItemId}?corporate=true')
        return res

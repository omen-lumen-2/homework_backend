import requests
import os


class BaseApiService(object):
    """
    Базовый класс для работы методов бизнес логики
    """
    def __init__(self):
        self.base_url = os.environ['BASE_URL']

    def _get(self, url, **kwargs):
        return requests.get(f"{self.base_url}{url}", **kwargs, verify=False )

    def _post(self, url, **kwargs):
        return requests.post(f"{self.base_url}{url}", **kwargs, verify=False)
import requests
import os


class BaseQaApi(object):
    """
    Базовый класс для работы методов qaApi
    """

    def __init__(self):
        self.base_url = os.environ['BASE_URL_QA_API']

    def _get(self, url, **kwargs):
        return requests.get(f"{self.base_url}{url}", **kwargs, verify=False )

    def _post(self, url, **kwargs):
        return requests.post(f"{self.base_url}{url}", **kwargs, verify=False)

    def _delete(self, url, **kwargs):
        return requests.delete(f"{self.base_url}{url}", **kwargs, verify=False)
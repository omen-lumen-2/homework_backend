import logging
import allure
import curlify
import json


class AssertableResponse(object):

    def __init__(self, response):
        self.response = response
        logging.info(f"\n\tcurl for request= {curlify.to_curl(response.request)}")
        logging.info(f"\n\tactual response code = {self.response.status_code}")
        logging.info(f"\n\tactual response body = {json.dumps(self.response.json(), indent=4, ensure_ascii=False)}")

    allure.step("ответ")

    def has_status_code(self, code):
        return self.response.status_code == code

    def get_json(self):
        assert self.response.headers['Content-Type'] == "application/json"
        return self.response.json()

    def get_san(self):
        _san = self.response.json()['san'] if 'san' in self.response.json() else False
        return _san
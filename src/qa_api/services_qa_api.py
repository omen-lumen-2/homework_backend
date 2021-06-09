import allure

from .base_qa_api import BaseQaApi
import curlify
import logging


class Service(BaseQaApi):

    def __init__(self):
        super().__init__()

    def delete_service_on_id(self, id):
        header = {'Accept': 'application/json'}
        return self._delete(f"/qa/services/{id}", headers=header)

    def delete_all_services(self):
        header = {'Accept': 'application/json'}
        return self._delete("/qa/services", headers=header)

    @allure.step("Создание услуги")
    def create_service(self, id, name, description, price, device_types):
        header = {'Accept': 'application/json'}
        json = {
            "id": id,
            "name": name,
            "description": description,
            "price": price,
            "device_types": device_types
        }
        r =self._post("/qa/services", json=json, headers=header)
        logging.info(f"Запрос на создание услуги")
        logging.info(f"\n\tcurl for request= {curlify.to_curl(r.request)}")
        logging.info(f"\n\tactual response code = {r.status_code}")
        return r


    def get_all_services(self):
        header = {'Accept': 'application/json'}
        return self._get("/qa/services", headers=header)

    def get_service_on_id(self, id):
        header = {'Accept': 'application/json'}
        return self._get(f"/qa/services/{id}", headers=header).json()
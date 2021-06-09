import allure

from .base_qa_api import BaseQaApi
import curlify
import  logging


class Movies(BaseQaApi):

    def __init__(self):
        super().__init__()

    def delete_film_on_id(self, id):
        header = {'Accept': 'application/json'}
        return self._delete(f"/qa/movies/{id}", headers=header)

    @allure.step("Создание фильма")
    def create_film(self, id, name, description, start_date, end_date, services_id):
        header = {'Accept': 'application/json'}
        json = {
            "id": id,
            "name": name,
            "description": description,
            "start_date": start_date,
            "end_date": end_date,
            "services": services_id
        }

        r = self._post(f"/qa/movies", json=json, headers=header)
        logging.info(f"Запрос на создание фильма")
        logging.info(f"\n\tcurl for request= {curlify.to_curl(r.request)}")
        logging.info(f"\n\tactual response code = {r.status_code}")
        return r


    def get_all_films(self):
        header = {'Accept': 'application/json'}
        return self._get("/qa/movies", headers=header)

    def get_films_on_id(self, id):
        header = {'Accept': 'application/json'}
        return self._get(f"/qa/movies/{id}", headers=header).json()

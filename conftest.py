import pytest
import logging
from src import Service, Movies


@pytest.fixture()
def get_service():
    service_id = []

    def _create_service(id, name, description, price, device_types):
        response = Service().create_service(id, name, description, price, device_types)
        assert response.status_code == 200
        id = response.json()["id"]
        service_id.append(id)
        logging.info(f"\n\tSaved id of service in fixture: {id}")
        return id

    yield _create_service

    for id in service_id:
        response = Service().delete_service_on_id(id)
        logging.info(f"\n\tStatus code deleting service with id({id}) : {response.status_code}")


@pytest.fixture()
def get_film():
    film_id = []

    def _create_film(id, name, description, start_date, end_date, services_id):
        response = Movies().create_film(id, name, description, start_date, end_date, services_id)
        logging.info(f"\n\tBody: {response.json()}")
        assert response.status_code == 200
        id = response.json()["id"]
        film_id.append(id)
        logging.info(f"\n\tSaved id of film in fixture: {id}")
        return id

    yield _create_film

    for id in film_id:
        response = Movies().delete_film_on_id(id)
        logging.info(f"\n\tStatus code deleting film with id({id}) : {response.status_code}")

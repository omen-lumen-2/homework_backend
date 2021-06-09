import allure

from .base_service import BaseApiService
from src import AssertableResponse
import logging


class TokenService(BaseApiService):
    """
    Класс для работы с токенами
    """

    def __init__(self):
        super().__init__()

    @allure.step("Выполнение запроса на получение токена")
    def create_token(self, device_type):
        """
        Выполнить запрос на создание токена для заданного типа устройства
        :param device_type: тип девайса
        """
        header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        json = {'device_type': device_type}
        logging.info(f"\t\nВыполнение запроса на получения токена с типом девайса: {device_type}")
        return AssertableResponse(
            self._post("/api/token", json=json, headers=header)
        )

    @allure.step("Получение токена")
    def get_token(self, device_type):
        """
        Получить токен для заданного типа устройства
        :param device_type: тип девайса
        """
        response = self.create_token(device_type)
        return response.get_json()["token"]
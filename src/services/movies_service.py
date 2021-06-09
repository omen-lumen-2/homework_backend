import allure

from .base_service import BaseApiService
from src import AssertableResponse
import logging


class MoviesService(BaseApiService):
    """
    Класс для работы с фильмами
    """

    def __init__(self):
        super().__init__()

    @allure.step("Получение списка доступных фильмов")
    def get_availible_films(self, token):
        """
        Получить список фильмов доступных для заданного токена
        :param token
        """
        header = {'Accept': 'application/json', 'X-TOKEN': token}
        logging.info(f"\t\nВыполнение запроса на получения доступных фильмов для токена: {token}")
        return AssertableResponse(
            self._get("/api/movies", headers=header)
        )


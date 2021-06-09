import pytest
from allure_commons.types import Severity

from src import TokenService, MoviesService, Service, Movies, WaitHelper, DataHelper
from hamcrest import *
import logging
import allure


@allure.suite("Тестовый набор для проверки получения доступных фильмов")
@allure.feature("Работа с контентом")
@allure.story("Получение доступных фильмов")
class TestMovies:

    @allure.severity(severity_level=Severity.MINOR)
    def test_get_films_without_token(self):
        # When
        response = MoviesService().get_availible_films(token=None)

        # Than
        assert response.has_status_code(403)
        assert response.get_json() == {"message": "'Токен не найден'"}

    @allure.severity(severity_level=Severity.CRITICAL)
    @pytest.mark.parametrize('device_type', ['tv', 'mobile', 'stb'])
    def test_get_film_for_different_device_type(self, device_type, get_service, get_film):
        # Given
        token = TokenService().get_token(device_type)

        service_id = get_service(1, "Name service", "Description service", 0, [device_type])

        WaitHelper().wait_untill(lambda: Service().get_all_services().json()['items'],
                                 has_item(has_entry('id', equal_to(service_id))), 10, 1, "Запрос списка услуг выполнен")

        film_id = get_film(1, "Name film", "Description film", DataHelper().get_data_with_offset(-1),
                           DataHelper().get_data_with_offset(1),
                           [service_id])

        WaitHelper().wait_untill(lambda: Movies().get_all_films().json()['items'],
                                 has_item(has_entry('id', equal_to(film_id))), 10, 1, "Запрос списка фильмов выполнен")

        # When

        response = MoviesService().get_availible_films(token=token)

        # Then
        response.has_status_code(200)

        service = Service().get_service_on_id(service_id)
        movie = Movies().get_films_on_id(film_id)
        assert_that(response.get_json()['items'], has_length(1))
        assert_that(response.get_json()['items'], has_item(has_entries(
            {"id": movie['id'],
             "name": movie['name'],
             "description": movie['description'],
             "start_date": movie['start_date'],
             "end_date": movie['end_date'],
             "services": [service]})))

    @allure.severity(severity_level=Severity.CRITICAL)
    @pytest.mark.parametrize(('start_day', 'end_day'),
                             [(DataHelper().get_data_with_offset(1), DataHelper().get_data_with_offset(2)),
                              (DataHelper().get_data_with_offset(-2), DataHelper().get_data_with_offset(-1))])
    def test_not_get_film_when_movie_not_availible_on_data(self, start_day, end_day, get_service, get_film):
        # Given
        device_type = 'tv'

        token = TokenService().get_token(device_type)

        service_id = get_service(1, "Name service", "Description service", 0, [device_type])

        WaitHelper().wait_untill(lambda: Service().get_all_services().json()['items'],
                                 has_item(has_entry('id', equal_to(service_id))), 10, 1, "Запрос списка услуг выполнен")

        film_id = get_film(1, "Name film", "Description film", start_day, end_day, [service_id])

        WaitHelper().wait_untill(lambda: Movies().get_all_films().json()['items'],
                                 has_item(has_entry('id', equal_to(film_id))), 10, 1, "Запрос списка фильмов выполнен")

        # When

        response = MoviesService().get_availible_films(token=token)

        # Then
        response.has_status_code(200)

        assert_that(response.get_json()['items'], has_length(0))

    @allure.severity(severity_level=Severity.NORMAL)
    def test_not_get_film_when_film_has_not_service(self, get_film):
        # Given
        device_type = 'tv'
        token = TokenService().get_token(device_type)

        film_id = get_film(1, "Name film", "Description film", DataHelper().get_data_with_offset(-1),
                           DataHelper().get_data_with_offset(1),
                           [])

        WaitHelper().wait_untill(lambda: Movies().get_all_films().json()['items'],
                                 has_item(has_entry('id', equal_to(film_id))), 10, 1, "Запрос списка фильмов выполнен")

        # When

        response = MoviesService().get_availible_films(token=token)

        # Then
        response.has_status_code(200)

        assert_that(response.get_json()['items'], has_length(0))

    @allure.severity(severity_level=Severity.CRITICAL)
    @pytest.mark.parametrize(('token_device_type', 'service_device_type'),
                             [('tv', ['mobile', 'stb']), ('mobile', ['tv', 'stb']), ('stb', ['mobile', 'tv'])])
    def test_not_get_film_when_service_has_not_current_type_device(self, token_device_type, service_device_type,
                                                                   get_film,
                                                                   get_service):
        # Given

        token = TokenService().get_token(token_device_type)

        service_id = get_service(1, "Name service", "Description service", 0, service_device_type)

        WaitHelper().wait_untill(lambda: Service().get_all_services().json()['items'],
                                 has_item(has_entry('id', equal_to(service_id))), 10, 1, "Запрос списка услуг выполнен")

        film_id = get_film(1, "Name film", "Description film", DataHelper().get_data_with_offset(-1),
                           DataHelper().get_data_with_offset(1),
                           [service_id])

        WaitHelper().wait_untill(lambda: Movies().get_all_films().json()['items'],
                                 has_item(has_entry('id', equal_to(film_id))), 10, 1, "Запрос списка фильмов выполнен")

        # When

        response = MoviesService().get_availible_films(token=token)

        # Then
        response.has_status_code(200)

        assert_that(response.get_json()['items'], has_length(0))

    @allure.severity(severity_level=Severity.NORMAL)
    def test_get_film_with_few_services(self, get_service, get_film):
        # Given
        device_type = 'tv'
        token = TokenService().get_token(device_type)

        first_service_id = get_service(1, "Name service one", "Description first service", 0, [device_type])

        WaitHelper().wait_untill(lambda: Service().get_all_services().json()['items'],
                                 has_item(has_entry('id', equal_to(first_service_id))), 10, 1,
                                 "Запрос списка услуг выполнен")
        second_service_id = get_service(1, "Name service two", "Description two service", 0, [device_type])

        WaitHelper().wait_untill(lambda: Service().get_all_services().json()['items'],
                                 has_item(has_entry('id', equal_to(second_service_id))), 10, 1,
                                 "Запрос списка услуг выполнен")

        film_id = get_film(1, "Name film", "Description film", DataHelper().get_data_with_offset(-1),
                           DataHelper().get_data_with_offset(1),
                           [first_service_id, second_service_id])

        WaitHelper().wait_untill(lambda: Movies().get_all_films().json()['items'],
                                 has_item(has_entry('id', equal_to(film_id))), 10, 1, "Запрос списка фильмов выполнен")

        # When

        response = MoviesService().get_availible_films(token=token)

        # Then
        response.has_status_code(200)

        first_service = Service().get_service_on_id(first_service_id)
        second_service = Service().get_service_on_id(second_service_id)
        movie = Movies().get_films_on_id(film_id)
        assert_that(response.get_json()['items'], has_length(1))
        assert_that(response.get_json()['items'], has_item(has_entries(
            {"id": movie['id'],
             "name": movie['name'],
             "description": movie['description'],
             "start_date": movie['start_date'],
             "end_date": movie['end_date']
             })))
        assert_that(response.get_json()['items'][0]['services'], has_item(first_service))
        assert_that(response.get_json()['items'][0]['services'], has_item(second_service))


    @allure.severity(severity_level=Severity.NORMAL)
    def test_get_few_films(self, get_service, get_film):
        # Given
        device_type = 'tv'
        token = TokenService().get_token(device_type)

        service_id = get_service(1, "Name service one", "Description first service", 0, [device_type])

        WaitHelper().wait_untill(lambda: Service().get_all_services().json()['items'],
                                 has_item(has_entry('id', equal_to(service_id))), 10, 1,
                                 "Запрос списка услуг выполнен")

        first_film_id = get_film(1, "Name first film", "Description first film", DataHelper().get_data_with_offset(-1),
                                 DataHelper().get_data_with_offset(1),
                                 [service_id])

        WaitHelper().wait_untill(lambda: Movies().get_all_films().json()['items'],
                                 has_item(has_entry('id', equal_to(first_film_id))), 10, 1,
                                 "Запрос списка фильмов выполнен")

        second_film_id = get_film(1, "Name second film", "Description second film", DataHelper().get_data_with_offset(-1),
                                  DataHelper().get_data_with_offset(1),
                                  [service_id])

        WaitHelper().wait_untill(lambda: Movies().get_all_films().json()['items'],
                                 has_item(has_entry('id', equal_to(second_film_id))), 10, 1,
                                 "Запрос списка фильмов выполнен")

        # When

        response = MoviesService().get_availible_films(token=token)

        # Then
        response.has_status_code(200)

        service = Service().get_service_on_id(service_id)
        first_movie = Movies().get_films_on_id(first_film_id)
        second_movie = Movies().get_films_on_id(second_film_id)
        assert_that(response.get_json()['items'], has_length(2))
        assert_that(response.get_json()['items'], has_item(has_entries(
            {"id": first_movie['id'],
             "name": first_movie['name'],
             "description": first_movie['description'],
             "start_date": first_movie['start_date'],
             "end_date": first_movie['end_date'],
             "services": [service]})))

        assert_that(response.get_json()['items'], has_item(has_entries(
            {"id": second_movie['id'],
             "name": second_movie['name'],
             "description": second_movie['description'],
             "start_date": second_movie['start_date'],
             "end_date": second_movie['end_date'],
             "services": [service]})))

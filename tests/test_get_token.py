import allure
import pytest
from allure_commons.types import Severity

from src import TokenService
from hamcrest import *


@allure.suite("Тестовый набор для проверки получения токена")
@allure.feature("Token")
@allure.story("Получение токена")
class TestToken:

    @allure.severity(severity_level=Severity.CRITICAL)
    @pytest.mark.parametrize('device_type', ['tv', 'mobile', 'stb'])
    def test_get_token_for_valid_type_of_devices(self, device_type):
        # When
        response = TokenService().create_token(device_type)

        # Then
        assert response.has_status_code(200)
        assert_that(response.get_json(), has_entry('token', is_(str)))
        assert_that(response.get_json(), has_length(1))

    @allure.severity(severity_level=Severity.MINOR)
    @pytest.mark.parametrize('device_type', ['tV', 'mobiles', None])
    def test_not_get_token_for_invalid_type_of_devices(self, device_type):
        # When
        response = TokenService().create_token(device_type)

        # Then
        assert response.has_status_code(200)
        assert_that(response.get_json(), has_entry('token', equal_to(None)))
        assert_that(response.get_json(), has_length(1))

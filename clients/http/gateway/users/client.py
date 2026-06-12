from datetime import time

from httpx import Response
from locust.env import Environment  # Импорт окружения Locust

from clients.http.client import HTTPClient, HTTPClientExtensions, build_gateway_locust_http_client, \
    build_gateway_http_client
import clients.http.gateway.client
from clients.http.gateway.users.schema import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)


class UsersGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/users сервиса http-gateway.
    """
    def create_user(self) -> CreateUserResponseSchema:
        # Генерация данных теперь происходит внутри схемы запроса
        request = CreateUserRequestSchema()
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)

    def get_user_api(self, user_id: str) -> Response:
        """
        Получить данные пользователя по его user_id.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/users/{user_id}")

    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Создание нового пользователя.

        :param request: Pydantic-модель с данными нового пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/users", json=request.model_dump(by_alias=True))

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        """
        Получить данные пользователя и вернуть как Pydantic-модель.

        :param user_id: Идентификатор пользователя.
        :return: Pydantic-модель с данными пользователя.
        """
        response = self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)

    def create_user(self) -> CreateUserResponseSchema:
        """
        Создать нового пользователя с автоматически сгенерированными данными.

        :return: Pydantic-модель с данными созданного пользователя.
        """
        request = CreateUserRequestSchema(
            email=f"user.{time.time()}@example.com",
            last_name="string",
            first_name="string",
            middle_name="string",
            phone_number="string"
        )
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersGatewayHTTPClient.
    """
    return UsersGatewayHTTPClient(client=build_gateway_http_client())

def build_users_gateway_http_client() -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию UsersGatewayHTTPClient.
    """
    return UsersGatewayHTTPClient(client=build_gateway_http_client())


# Новый билдер для нагрузочного тестирования
def build_users_gateway_locust_http_client(environment: Environment) -> UsersGatewayHTTPClient:
    """
    Функция создаёт экземпляр UsersGatewayHTTPClient адаптированного под Locust.

    Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
    Используется исключительно в нагрузочных тестах.

    :param environment: объект окружения Locust.
    :return: экземпляр UsersGatewayHTTPClient с хуками сбора метрик.
    """
    return UsersGatewayHTTPClient(client=build_gateway_locust_http_client(environment))


class CardsGatewayHTTPClient:
    pass


class VirtualCardRequest:
    pass


class PhysicalCardRequest:
    pass
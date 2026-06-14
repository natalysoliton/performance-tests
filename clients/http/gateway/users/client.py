from httpx import Response
from locust.env import Environment

from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.client import (
    build_gateway_http_client,
    build_gateway_locust_http_client
)
from clients.http.gateway.users.schema import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)
from tools.routes import APIRoutes  # Импортируем enum APIRoutes


class UsersGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/users сервиса http-gateway.
    """

    def get_user_api(self, user_id: str) -> Response:
        """
        Получить данные пользователя по его user_id.

        :param user_id: Идентификатор пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        # Вместо /api/v1/users используем APIRoutes.USERS
        return self.get(
            f"{APIRoutes.USERS}/{user_id}",
            extensions=HTTPClientExtensions(route=f"{APIRoutes.USERS}/{{user_id}}")
        )

    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Создание нового пользователя.

        :param request: Pydantic-модель с данными нового пользователя.
        :return: Ответ от сервера (объект httpx.Response).
        """
        # Вместо /api/v1/users используем APIRoutes.USERS
        return self.post(APIRoutes.USERS, json=request.model_dump(by_alias=True))

    def create_user(self) -> CreateUserResponseSchema:
        # Генерация данных теперь происходит внутри схемы запроса
        request = CreateUserRequestSchema()
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)

    def get_user(self, user_id: str) -> GetUserResponseSchema:
        """
        Получить данные пользователя и вернуть как Pydantic-модель.

        :param user_id: Идентификатор пользователя.
        :return: Pydantic-модель с данными пользователя.
        """
        response = self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)


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

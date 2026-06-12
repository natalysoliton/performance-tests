from httpx import Response, QueryParams
from locust.env import Environment  # Импорт окружения Locust

from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.accounts.schema import (
    GetAccountsQuerySchema,
    GetAccountsResponseSchema,
    OpenDepositAccountRequestSchema,
    OpenDepositAccountResponseSchema,
    OpenSavingsAccountRequestSchema,
    OpenSavingsAccountResponseSchema,
    OpenDebitCardAccountRequestSchema,
    OpenDebitCardAccountResponseSchema,
    OpenCreditCardAccountRequestSchema,
    OpenCreditCardAccountResponseSchema
)
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.users.schema import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)
from clients.http.gateway.client import (
    build_gateway_http_client,
    build_gateway_locust_http_client  # Импорт билдера для нагрузочного тестирования
)

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

        return self.get(
            f"/api/v1/users/{user_id}",
            extensions=HTTPClientExtensions(route="/api/v1/users/{user_id}")  # Явно передаём логическое имя маршрута
        )

class AccountsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/accounts сервиса http-gateway.

    Предоставляет методы для работы со счетами:
    - Получение списка счетов пользователя
    - Открытие депозитного счета
    - Открытие сберегательного счета
    - Открытие дебетового счета
    - Открытие кредитного счета
    """

    def get_accounts_api(self, query: GetAccountsQuerySchema) -> Response:
        """
        Выполняет GET-запрос на получение списка счетов пользователя.

        :param query: Pydantic-модель с параметрами запроса, например: {'userId': '123'}.
        :return: Объект httpx.Response с данными о счетах.
        """
        return self.get(
            "/api/v1/accounts",
            params=QueryParams(**query.model_dump(by_alias=True))
        )

    def open_deposit_account_api(self, request: OpenDepositAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия депозитного счёта.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(
            "/api/v1/accounts/open-deposit-account",
            json=request.model_dump(by_alias=True)
        )

    def open_savings_account_api(self, request: OpenSavingsAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия сберегательного счёта.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response.
        """
        return self.post(
            "/api/v1/accounts/open-savings-account",
            json=request.model_dump(by_alias=True)
        )

    def open_debit_card_account_api(self, request: OpenDebitCardAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия дебетовой карты.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response.
        """
        return self.post(
            "/api/v1/accounts/open-debit-card-account",
            json=request.model_dump(by_alias=True)
        )

    def open_credit_card_account_api(self, request: OpenCreditCardAccountRequestSchema) -> Response:
        """
        Выполняет POST-запрос для открытия кредитной карты.

        :param request: Pydantic-модель с userId.
        :return: Объект httpx.Response.
        """
        return self.post(
            "/api/v1/accounts/open-credit-card-account",
            json=request.model_dump(by_alias=True)
        )

    def get_accounts(self, user_id: str) -> GetAccountsResponseSchema:
        """
        Получает список всех счетов пользователя.

        :param user_id: ID пользователя.
        :return: Pydantic-модель со списком счетов.
        """
        query = GetAccountsQuerySchema(user_id=user_id)
        response = self.get_accounts_api(query)
        return GetAccountsResponseSchema.model_validate_json(response.text)

    def open_deposit_account(self, user_id: str) -> OpenDepositAccountResponseSchema:
        """
        Открывает депозитный счет для пользователя.

        :param user_id: ID пользователя.
        :return: Pydantic-модель с информацией об открытом счете.
        """
        request = OpenDepositAccountRequestSchema(user_id=user_id)
        response = self.open_deposit_account_api(request)
        return OpenDepositAccountResponseSchema.model_validate_json(response.text)

    def open_savings_account(self, user_id: str) -> OpenSavingsAccountResponseSchema:
        """
        Открывает сберегательный счет для пользователя.

        :param user_id: ID пользователя.
        :return: Pydantic-модель с информацией об открытом счете.
        """
        request = OpenSavingsAccountRequestSchema(user_id=user_id)
        response = self.open_savings_account_api(request)
        return OpenSavingsAccountResponseSchema.model_validate_json(response.text)

    def open_debit_card_account(self, user_id: str) -> OpenDebitCardAccountResponseSchema:
        """
        Открывает дебетовый счет для пользователя.

        :param user_id: ID пользователя.
        :return: Pydantic-модель с информацией об открытом счете.
        """
        request = OpenDebitCardAccountRequestSchema(user_id=user_id)
        response = self.open_debit_card_account_api(request)
        return OpenDebitCardAccountResponseSchema.model_validate_json(response.text)

    def open_credit_card_account(self, user_id: str) -> OpenCreditCardAccountResponseSchema:
        """
        Открывает кредитный счет для пользователя.

        :param user_id: ID пользователя.
        :return: Pydantic-модель с информацией об открытом счете.
        """
        request = OpenCreditCardAccountRequestSchema(user_id=user_id)
        response = self.open_credit_card_account_api(request)
        return OpenCreditCardAccountResponseSchema.model_validate_json(response.text)


def build_accounts_gateway_http_client() -> AccountsGatewayHTTPClient:
    """
    Функция создаёт экземпляр AccountsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию AccountsGatewayHTTPClient.
    """

    def build_accounts_gateway_http_client() -> AccountsGatewayHTTPClient:
        """
        Функция создаёт экземпляр AccountsGatewayHTTPClient с уже настроенным HTTP-клиентом.

        :return: Готовый к использованию AccountsGatewayHTTPClient.
        """
        return AccountsGatewayHTTPClient(client=build_gateway_http_client())

    # Новый билдер для нагрузочного тестирования
    def build_accounts_gateway_locust_http_client(environment: Environment) -> AccountsGatewayHTTPClient:
        """
        Функция создаёт экземпляр AccountsGatewayHTTPClient адаптированного под Locust.

        Клиент автоматически собирает метрики и передаёт их в Locust через хуки.
        Используется исключительно в нагрузочных тестах.

        :param environment: объект окружения Locust.
        :return: экземпляр AccountsGatewayHTTPClient с хуками сбора метрик.
        """
        return AccountsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))


def build_accounts_gateway_locust_http_client():
    return None
from locust import User, between, task

from clients.http.gateway.users.client import (
    build_users_gateway_locust_http_client,
    UsersGatewayHTTPClient
)
from clients.http.gateway.accounts.client import (
    build_accounts_gateway_locust_http_client,
    AccountsGatewayHTTPClient
)
from clients.http.gateway.accounts.schema import OpenDebitCardAccountRequestSchema


class OpenDebitCardAccountScenarioUser(User):
    """
    Виртуальный пользователь, использующий кастомные API-клиенты.

    Сценарий:
    1. При старте (on_start) создаёт нового пользователя через UsersGatewayHTTPClient
    2. В задаче @task открывает дебетовый счёт через AccountsGatewayHTTPClient

    Метрики собираются автоматически через event hooks HTTPX.
    """

    # Фиктивное поле host (требование Locust, не используется т.к. у нас свой клиент)
    host = "localhost"

    # Пауза между задачами (имитация реального поведения пользователя)
    wait_time = between(1, 3)

    # Клиенты API (будут инициализированы в on_start)
    users_gateway_client: UsersGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient

    # Сохраняем ID созданного пользователя
    user_id: str = None

    def on_start(self) -> None:
        """
        Выполняется один раз при запуске каждого виртуального пользователя.

        Создаём API-клиенты с поддержкой метрик Locust и
        создаём нового пользователя через API.
        """
        # Шаг 1: Инициализируем API-клиенты с привязкой к окружению Locust
        # Передаём self.environment, чтобы клиенты могли отправлять метрики в Locust
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.environment)

        # Шаг 2: Создаём пользователя через кастомный API-клиент
        # Метод create_user() автоматически генерирует фейковые данные
        create_user_response = self.users_gateway_client.create_user()

        # Шаг 3: Сохраняем ID созданного пользователя для использования в задаче
        self.user_id = create_user_response.user.id

    @task
    def open_debit_card_account(self) -> None:
        """
        Основная нагрузочная задача: открытие дебетового счёта.

        Выполняет запрос POST /api/v1/accounts/open-debit-card-account
        с использованием сохранённого user_id.
        """
        if self.user_id is None:
            # Если по какой-то причине пользователь не создан, пропускаем задачу
            return

        # Формируем запрос на открытие счёта с использованием Pydantic-модели
        request_data = OpenDebitCardAccountRequestSchema(userId=self.user_id)

        # Отправляем запрос через кастомный API-клиент
        # Метрики (время ответа, статус, ошибки) собираются автоматически через event hooks
        self.accounts_gateway_client.open_debit_card_account_api(request_data)

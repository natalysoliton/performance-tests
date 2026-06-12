from locust import User, between, task

from clients.grpc.gateway.users.client import (
    build_users_gateway_locust_grpc_client,
    UsersGatewayGRPCClient
)
from clients.grpc.gateway.accounts.client import (
    build_accounts_gateway_locust_grpc_client,
    AccountsGatewayGRPCClient
)
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse


class OpenDebitCardAccountScenarioUser(User):
    """
    Виртуальный пользователь для нагрузочного тестирования gRPC API.

    Сценарий:
    1. При старте (on_start) создаёт gRPC клиенты с интерцепторами для сбора метрик
    2. Создаёт нового пользователя через UsersGatewayGRPCClient
    3. В основной задаче (@task) открывает дебетовый счёт через AccountsGatewayGRPCClient

    Метрики собираются автоматически через LocustInterceptor.
    """

    # Атрибут host обязателен для Locust, даже если не используется напрямую в gRPC
    host = "localhost"

    # Время ожидания между выполнением задач (имитация реального поведения пользователя)
    wait_time = between(1, 3)

    # Аннотации типов для клиентов
    users_gateway_client: UsersGatewayGRPCClient
    accounts_gateway_client: AccountsGatewayGRPCClient

    # Аннотация для ответа от create_user
    create_user_response: CreateUserResponse

    def on_start(self) -> None:
        """
        Метод, вызываемый при старте каждого виртуального пользователя.

        Здесь происходит:
        1. Инициализация gRPC API клиентов с интерцепторами для сбора метрик
        2. Создание тестового пользователя (один раз за сессию)
        """
        # Создаём gRPC-клиенты, адаптированные для Locust с интерцепторами метрик
        # Передаём self.environment для связи с системой сбора статистики
        self.users_gateway_client = build_users_gateway_locust_grpc_client(self.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_grpc_client(self.environment)

        # Создаём пользователя один раз в начале сессии
        # Все данные генерируются автоматически внутри клиента
        self.create_user_response = self.users_gateway_client.create_user()

        # Опционально: вывод информации о созданном пользователе (для отладки)
        # print(f"[DEBUG] Создан пользователь с ID: {self.create_user_response.user.id}")

    @task
    def open_debit_card_account(self) -> None:
        """
        Основная нагрузочная задача виртуального пользователя.

        Открывает дебетовый счёт для созданного пользователя.
        Метод будет многократно вызываться Locust в соответствии с параметрами нагрузки.

        Метрики вызова (время выполнения, статус, ошибки) собираются автоматически
        через LocustInterceptor, внедрённый в gRPC канал.
        """
        # Получаем ID пользователя из ответа, сохранённого при создании
        user_id = self.create_user_response.user.id

        # Выполняем gRPC запрос на открытие дебетового счёта
        # Интерцептор автоматически замеряет время и отправляет метрику в Locust
        self.accounts_gateway_client.open_debit_card_account(user_id)
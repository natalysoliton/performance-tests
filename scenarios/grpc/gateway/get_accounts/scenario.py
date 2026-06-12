"""
Нагрузочный сценарий для тестирования получения списка счетов через gRPC API.

Сценарий выполняет в произвольном порядке:
1. Создание пользователя (вес 2)
2. Открытие депозитного счёта (вес 2)
3. Получение списка всех счетов (вес 6)

Использует базовый GatewayGRPCTaskSet для централизованной инициализации клиентов
и LocustBaseUser для общих настроек виртуального пользователя.
"""

from locust import task

# Импортируем базовый TaskSet для gRPC
from clients.grpc.gateway.locust import GatewayGRPCTaskSet

# Импортируем базового пользователя Locust
from tools.locust.user import LocustBaseUser

# Импортируем схемы ответов для типизации shared state
from contracts.services.gateway.accounts.rpc_open_deposit_account_pb2 import (
    OpenDepositAccountResponse
)
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse


class GetAccountsTaskSet(GatewayGRPCTaskSet):
    """
    Нагрузочный сценарий для gRPC API, выполняющий в произвольном порядке:
    1. Создание пользователя (вес 2)
    2. Открытие депозитного счёта (вес 2)
    3. Получение списка счетов (вес 6)

    Использует базовый GatewayGRPCTaskSet и уже созданных в нём API клиентов.

    Важно: Все задачи выполняются в произвольном порядке, поэтому необходимо
    проверять наличие shared state перед выполнением зависимых задач.
    """

    # Shared state — сохраняем результаты запросов для дальнейшего использования
    create_user_response: CreateUserResponse | None = None
    open_deposit_account_response: OpenDepositAccountResponse | None = None

    @task(2)
    def create_user(self) -> None:
        """
        Задача: Создание нового пользователя.

        Вес: 2
        Создаёт пользователя через gRPC API клиент и сохраняет ответ
        для использования в других задачах.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self) -> None:
        """
        Задача: Открытие депозитного счёта.

        Вес: 2
        Открывает депозитный счёт для созданного пользователя.
        Выполняется только если пользователь уже создан.
        """
        # Защита от сбоев: если пользователь не был создан, пропускаем задачу
        if not self.create_user_response:
            return

        # Открываем депозитный счёт для пользователя
        self.open_deposit_account_response = self.accounts_gateway_client.open_deposit_account(
            user_id=self.create_user_response.user.id
        )

    @task(6)
    def get_accounts(self) -> None:
        """
        Задача: Получение списка счетов.

        Вес: 6
        Запрашивает список всех счетов для текущего пользователя.
        Выполняется только если пользователь уже создан.

        Примечание: Эта задача имеет наибольший вес (6), так как получение
        списка счетов — наиболее частая операция в реальном сценарии.
        """
        # Защита от сбоев: если пользователь не был создан, пропускаем задачу
        if not self.create_user_response:
            return

        # Получаем список счетов пользователя
        self.accounts_gateway_client.get_accounts(
            user_id=self.create_user_response.user.id
        )


class GetAccountsScenarioUser(LocustBaseUser):
    """
    Пользователь Locust, исполняющий сценарий получения списка счетов через gRPC API.

    Наследует от LocustBaseUser:
    - host = "localhost" (фиктивное значение)
    - wait_time = between(1, 3)

    Задачи выполняются в произвольном порядке с весами:
    - create_user: 2
    - open_deposit_account: 2
    - get_accounts: 6
    """

    # Задачи, которые будет выполнять пользователь
    tasks = [GetAccountsTaskSet]
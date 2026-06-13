from locust import task

from clients.grpc.gateway.locust import GatewayGRPCSequentialTaskSet
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import (
    OpenDebitCardAccountResponse
)
from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import (
    IssuePhysicalCardResponse
)
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse
from tools.locust.user import LocustBaseUser


class IssuePhysicalCardSequentialTaskSet(GatewayGRPCSequentialTaskSet):
    """
    Последовательный gRPC сценарий для нового пользователя, оформляющего физическую карту.

    Шаги выполняются строго по порядку:
    1. create_user - создание пользователя
    2. open_debit_card_account - открытие дебетового счёта
    3. issue_physical_card - выпуск физической карты
    """

    # Shared state — сохраняем результаты для использования в следующих шагах
    create_user_response: CreateUserResponse | None = None
    open_debit_card_account_response: OpenDebitCardAccountResponse | None = None
    issue_physical_card_response: IssuePhysicalCardResponse | None = None

    @task
    def create_user(self) -> None:
        """
        Шаг 1: Создание нового пользователя.

        Создаёт пользователя через gRPC API клиент.
        Сохраняет ответ для использования в следующих шагах.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self) -> None:
        """
        Шаг 2: Открытие дебетового счёта.

        Открывает дебетовый счёт для созданного пользователя.
        Выполняется только если пользователь успешно создан.
        """
        if not self.create_user_response:
            return

        self.open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )

    @task
    def issue_physical_card(self) -> None:
        """
        Шаг 3: Выпуск физической карты.

        Выпускает физическую карту, привязанную к дебетовому счёту.
        Выполняется только если счёт успешно открыт.
        """
        if not self.open_debit_card_account_response:
            return

        self.issue_physical_card_response = self.cards_gateway_client.issue_physical_card(
            user_id=self.create_user_response.user.id,
            account_id=self.open_debit_card_account_response.account.id
        )


class IssuePhysicalCardScenarioUser(LocustBaseUser):
    """
    Пользователь Locust, исполняющий gRPC сценарий выпуска физической карты.

    Наследует от LocustBaseUser:
    - host = "localhost" (фиктивное значение)
    - wait_time = between(1, 3)

    Задачи выполняются строго последовательно в порядке, определённом в
    IssuePhysicalCardSequentialTaskSet.
    """

    # Задачи, которые будет выполнять пользователь
    tasks = [IssuePhysicalCardSequentialTaskSet]
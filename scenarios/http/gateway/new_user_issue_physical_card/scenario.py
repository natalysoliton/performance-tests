from locust import task

from clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema
from clients.http.gateway.cards.schema import IssuePhysicalCardResponseSchema
from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema
from tools.locust.user import LocustBaseUser


class IssuePhysicalCardSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    """
    Последовательный сценарий для нового пользователя, оформляющего физическую карту.

    Шаги выполняются строго по порядку:
    1. create_user - создание пользователя
    2. open_debit_card_account - открытие дебетового счёта
    3. issue_physical_card - выпуск физической карты
    """

    # Shared state — сохраняем результаты для использования в следующих шагах
    create_user_response: CreateUserResponseSchema | None = None
    open_debit_card_account_response: OpenDebitCardAccountResponseSchema | None = None
    issue_physical_card_response: IssuePhysicalCardResponseSchema | None = None

    @task
    def create_user(self) -> None:
        """
        Шаг 1: Создание нового пользователя.

        Создаёт пользователя через HTTP API клиент.
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
    Пользователь Locust, исполняющий сценарий выпуска физической карты.

    Наследует от LocustBaseUser:
    - host = "localhost" (фиктивное значение)
    - wait_time = between(1, 3)

    Задачи выполняются строго последовательно в порядке, определённом в
    IssuePhysicalCardSequentialTaskSet.
    """

    # Задачи, которые будет выполнять пользователь
    tasks = [IssuePhysicalCardSequentialTaskSet]

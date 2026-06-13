from locust import task, events
from locust.env import Environment

from clients.grpc.gateway.locust import GatewayGRPCTaskSet
from seeds.scenarios.existing_user_get_operations import ExistingUserGetOperationsSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


# Хук инициализации — вызывается один раз перед началом запуска нагрузки
@events.init.add_listener
def init(environment: Environment, **kwargs) -> None:
    """
    Инициализация сидинга перед запуском нагрузочного теста.

    Выполняется один раз:
    1. Генерирует тестовые данные (250 пользователей с дебетовыми и сберегательными счетами)
    2. Сохраняет результат в JSON-файл
    3. Загружает данные в environment.seeds для использования виртуальными пользователями
    """
    print("=" * 60)
    print("Выполнение сидинга перед запуском нагрузочного теста...")
    print("=" * 60)

    # Выполняем сидинг
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()  # создаём пользователей, счета, карты

    # Загружаем результат сидинга (из файла JSON) и сохраняем в окружение Locust
    environment.seeds = seeds_scenario.load()

    print(f"Сидинг завершён. Загружено пользователей: {len(environment.seeds.users)}")
    print("=" * 60)


class GetOperationsTaskSet(GatewayGRPCTaskSet):
    """
    Набор задач для существующего пользователя, получающего операции и статистику.

    Задачи выполняются в произвольном порядке с заданными весами:
    - get_accounts: вес 3 (проверка баланса - самое частое действие)
    - get_operations: вес 2 (просмотр истории операций)
    - get_operations_summary: вес 1 (просмотр статистики - реже)
    """

    seed_user: SeedUserResult  # Типизированная ссылка на данные из сидинга

    def on_start(self) -> None:
        """
        Вызывается при старте каждого виртуального пользователя.

        1. Вызывает родительский on_start() для инициализации API-клиентов
        2. Получает случайного пользователя из подготовленного списка сидинга
        """
        super().on_start()
        # Получаем случайного пользователя из подготовленного списка
        self.seed_user = self.user.environment.seeds.get_random_user()

    @task(3)
    def get_accounts(self) -> None:
        """
        Задача: Получение списка счетов.

        Вес: 3 (самое частое действие)
        Запрашивает список всех счетов пользователя.
        Пользователи часто проверяют баланс, поэтому это действие самое популярное.
        """
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(2)
    def get_operations(self) -> None:
        """
        Задача: Получение списка операций.

        Вес: 2 (средняя частота)
        Запрашивает список всех операций по дебетовому счёту пользователя.
        Пользователи проверяют историю операций, чтобы убедиться в прохождении платежей.
        """
        # Используем дебетовый счёт, так как он есть у каждого пользователя
        account_id = self.seed_user.debit_card_accounts[0].account_id
        self.operations_gateway_client.get_operations(account_id=account_id)

    @task(1)
    def get_operations_summary(self) -> None:
        """
        Задача: Получение статистики операций.

        Вес: 1 (наименее частое действие)
        Запрашивает агрегированную статистику по операциям пользователя.
        Пользователи реже заходят в раздел статистики расходов.
        """
        account_id = self.seed_user.debit_card_accounts[0].account_id
        self.operations_gateway_client.get_operations_summary(account_id=account_id)


class GetOperationsScenarioUser(LocustBaseUser):
    """
    Пользователь Locust, исполняющий gRPC сценарий получения операций и статистики.

    Наследует от LocustBaseUser:
    - host = "localhost" (фиктивное значение)
    - wait_time = between(1, 3)

    Задачи выполняются в произвольном порядке с весами:
    - get_accounts: 3 (50%)
    - get_operations: 2 (33.3%)
    - get_operations_summary: 1 (16.7%)
    """

    # Задачи, которые будет выполнять пользователь
    tasks = [GetOperationsTaskSet]
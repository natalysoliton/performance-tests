from locust import task, events
from locust.env import Environment

from clients.http.gateway.locust import GatewayHTTPTaskSet
from seeds.scenarios.existing_user_issue_virtual_card import ExistingUserIssueVirtualCardSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


# Хук инициализации — вызывается один раз перед началом запуска нагрузки
@events.init.add_listener
def init(environment: Environment, **kwargs) -> None:
    """
    Инициализация сидинга перед запуском нагрузочного теста.

    Выполняется один раз:
    1. Генерирует тестовые данные (150 пользователей с дебетовыми счетами)
    2. Сохраняет результат в JSON-файл
    3. Загружает данные в environment.seeds для использования виртуальными пользователями
    """
    print("=" * 60)
    print("Выполнение сидинга перед запуском нагрузочного теста...")
    print("=" * 60)

    # Выполняем сидинг
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()  # создаём пользователей и счета

    # Загружаем результат сидинга (из файла JSON) и сохраняем в окружение Locust
    environment.seeds = seeds_scenario.load()

    print(f"Сидинг завершён. Загружено пользователей: {len(environment.seeds.users)}")
    print("=" * 60)


class IssueVirtualCardTaskSet(GatewayHTTPTaskSet):
    """
    Набор задач для существующего пользователя, выпускающего виртуальную карту.

    Задачи выполняются в произвольном порядке с заданными весами:
    - get_accounts: вес 3 (проверка баланса - часто)
    - issue_virtual_card: вес 1 (выпуск карты - редко, но критично)

    Обоснование весов:
    - Выпуск карты - действие, которое пользователь выполняет один раз за сессию
    - Проверка счетов происходит чаще - пользователь обновляет страницу,
      чтобы убедиться, что карта появилась в списке
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

        Вес: 3 (выполняется чаще)
        Запрашивает список всех счетов пользователя.
        Пользователи часто проверяют баланс и обновляют страницу,
        чтобы увидеть новую карту в списке.
        """
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(1)
    def issue_virtual_card(self) -> None:
        """
        Задача: Выпуск виртуальной карты.

        Вес: 1 (выполняется реже, но критически важно)
        Выпускает новую виртуальную карту для пользователя.
        Это действие выполняется один раз за сессию пользователя.
        """
        # Используем дебетовый счёт пользователя для выпуска карты
        self.cards_gateway_client.issue_virtual_card(
            user_id=self.seed_user.user_id,
            account_id=self.seed_user.debit_card_accounts[0].account_id
        )


class IssueVirtualCardScenarioUser(LocustBaseUser):
    """
    Пользователь Locust, исполняющий сценарий выпуска виртуальной карты.

    Наследует от LocustBaseUser:
    - host = "localhost" (фиктивное значение)
    - wait_time = between(1, 3)

    Задачи выполняются в произвольном порядке с весами:
    - get_accounts: 3 (75%)
    - issue_virtual_card: 1 (25%)
    """

    # Задачи, которые будет выполнять пользователь
    tasks = [IssueVirtualCardTaskSet]
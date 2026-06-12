"""
Сценарий сидинга для существующего пользователя, который выпускает виртуальную карту.

Создаёт 300 пользователей, каждому из которых открывает дебетовый счёт.
Данные сохраняются в файл для последующего использования в нагрузочных тестах.
"""

from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan


class ExistingUserIssueVirtualCardSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который выпускает виртуальную карту.
    Создаёт 300 пользователей, каждому открывает дебетовый счёт.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        План сидинга, который описывает, сколько пользователей нужно создать
        и какие именно данные для них генерировать.

        В данном случае:
        - Создаём 300 пользователей
        - Каждому пользователю открываем 1 дебетовый счёт

        Returns:
            SeedsPlan: План генерации данных
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Количество пользователей
                debit_card_accounts=SeedAccountsPlan(
                    count=1  # Количество дебетовых счетов на пользователя
                )
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Название сценария сидинга, которое будет использоваться для сохранения данных.

        Returns:
            str: Имя сценария
        """
        return "existing_user_issue_virtual_card"


if __name__ == '__main__':
    """
    Запуск сценария сидинга вручную.
    Создаём объект сценария и вызываем метод build для создания данных.

    Команда для запуска:
        python -m seeds.scenarios.existing_user_issue_virtual_card
    """
    print("=" * 60)
    print("Запуск сидинга для сценария: existing_user_issue_virtual_card")
    print("=" * 60)

    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()

    print("\n" + "=" * 60)
    print("Сидинг успешно завершён!")
    print("Результат сохранён в: dumps/existing_user_issue_virtual_card_seeds.json")
    print("=" * 60)
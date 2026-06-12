"""
Сценарий сидинга для существующего пользователя, который просматривает операции.

Создаёт 300 пользователей, каждому из которых открывает кредитный счёт
и генерирует операции:
- 5 операций покупки
- 1 операция пополнения счёта
- 1 операция снятия наличных

Данные сохраняются в файл для последующего использования в нагрузочных тестах.
"""

from seeds.scenario import SeedsScenario
from seeds.schema.plan import (
    SeedsPlan,
    SeedUsersPlan,
    SeedAccountsPlan,
    SeedCardsPlan,
    SeedOperationsPlan
)


class ExistingUserGetOperationsSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который просматривает операции.
    Создаёт 300 пользователей, каждому открывает кредитный счёт
    и генерирует операции покупки, пополнения и снятия наличных.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        План сидинга, который описывает, сколько пользователей нужно создать
        и какие именно данные для них генерировать.

        В данном случае:
        - Создаём 300 пользователей
        - Каждому пользователю открываем 1 кредитный счёт
        - На каждом счёте генерируем:
            - 5 операций покупки
            - 1 операцию пополнения
            - 1 операцию снятия наличных

        Returns:
            SeedsPlan: План генерации данных
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Количество пользователей
                credit_card_accounts=SeedAccountsPlan(
                    count=1,  # Количество кредитных счетов на пользователя
                    purchase_operations=SeedOperationsPlan(count=5),  # 5 операций покупки
                    top_up_operations=SeedOperationsPlan(count=1),  # 1 операция пополнения
                    cash_withdrawal_operations=SeedOperationsPlan(count=1)  # 1 операция снятия наличных
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
        return "existing_user_get_operations"


if __name__ == '__main__':
    """
    Запуск сценария сидинга вручную.
    Создаём объект сценария и вызываем метод build для создания данных.

    Команда для запуска:
        python -m seeds.scenarios.existing_user_get_operations
    """
    print("=" * 60)
    print("Запуск сидинга для сценария: existing_user_get_operations")
    print("=" * 60)

    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()

    print("\n" + "=" * 60)
    print("Сидинг успешно завершён!")
    print("Результат сохранён в: dumps/existing_user_get_operations_seeds.json")
    print("=" * 60)

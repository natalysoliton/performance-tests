"""
Функции для сохранения и загрузки результатов сидинга в JSON-файлы.
"""

import os

from seeds.schema.result import SeedsResult
from tools.logger import get_logger

# Создаём логгер для отслеживания операций с файлами сидинга
logger = get_logger("SEEDS_DUMPS")


def save_seeds_result(result: SeedsResult, scenario: str) -> None:
    """
    Сохраняет результат сидинга (SeedsResult) в JSON-файл.

    :param result: Результат сидинга, сгенерированный билдером.
    :param scenario: Название сценария нагрузки, для которого создаются данные.
                     Используется для генерации имени файла (например, "credit_card_test").
    """
    # Формируем путь к файлу
    seeds_file = f"./dumps/{scenario}_seeds.json"

    # Убедимся, что папка dumps существует
    if not os.path.exists("dumps"):
        os.mkdir("dumps")
        logger.debug(f"Created directory: dumps")

    # Сохраняем результат сидинга в файл
    with open(seeds_file, 'w+', encoding="utf-8") as file:
        file.write(result.model_dump_json())

    # Логируем успешное сохранение
    logger.debug(f"Seeding result saved to file: {seeds_file}")


def load_seeds_result(scenario: str) -> SeedsResult:
    """
    Загружает результат сидинга из JSON-файла.

    :param scenario: Название сценария нагрузки, данные которого нужно загрузить.
    :return: Объект SeedsResult, восстановленный из файла.
    """
    # Формируем путь к файлу
    seeds_file = f'./dumps/{scenario}_seeds.json'

    # Открываем файл и валидируем его как объект SeedsResult
    with open(seeds_file, 'r', encoding="utf-8") as file:
        result = SeedsResult.model_validate_json(file.read())

    # Логируем успешную загрузку
    logger.debug(f"Seeding result loaded from file: {seeds_file}")

    return result
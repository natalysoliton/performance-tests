#!/usr/bin/env python3
"""
Скрипт для получения документов по счету.

Выполняет последовательность действий:
1. Создание пользователя
2. Открытие кредитного счёта
3. Получение документа тарифа
4. Получение документа контракта
"""

import logging
import sys
from typing import Dict, Any

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def build_users_gateway_http_client():
    """
    Создание и настройка клиента для работы с API пользователей.
    
    Returns:
        UsersGatewayHTTPClient: Настроенный клиент для работы с пользователями
    """
    try:
        from clients.http.gateway.users import UsersGatewayHTTPClient
        client = UsersGatewayHTTPClient(base_url="http://localhost:8080")
        logger.info("UsersGatewayHTTPClient успешно создан")
        return client
    except ImportError as e:
        logger.error(f"Ошибка импорта UsersGatewayHTTPClient: {e}")
        raise


def build_accounts_gateway_http_client():
    """
    Создание и настройка клиента для работы с API счетов.
    
    Returns:
        AccountsGatewayHTTPClient: Настроенный клиент для работы со счетами
    """
    try:
        from clients.http.gateway.accounts import AccountsGatewayHTTPClient
        client = AccountsGatewayHTTPClient(base_url="http://localhost:8080")
        logger.info("AccountsGatewayHTTPClient успешно создан")
        return client
    except ImportError as e:
        logger.error(f"Ошибка импорта AccountsGatewayHTTPClient: {e}")
        raise


def build_documents_gateway_http_client():
    """
    Создание и настройка клиента для работы с API документов.
    
    Returns:
        DocumentsGatewayHTTPClient: Настроенный клиент для работы с документами
    """
    try:
        from clients.http.gateway.documents import DocumentsGatewayHTTPClient
        client = DocumentsGatewayHTTPClient(base_url="http://localhost:8080")
        logger.info("DocumentsGatewayHTTPClient успешно создан")
        return client
    except ImportError as e:
        logger.error(f"Ошибка импорта DocumentsGatewayHTTPClient: {e}")
        raise


def create_user(client) -> Dict[str, Any]:
    """
    Создание нового пользователя.
    
    Args:
        client: Клиент для работы с API пользователей
        
    Returns:
        Dict[str, Any]: Ответ от API с информацией о созданном пользователе
    """
    try:
        from clients.http.gateway.users import CreateUserRequestDict
        
        # Подготовка данных для создания пользователя
        user_request: CreateUserRequestDict = {
            "email": f"user.{int(__import__('time').time())}@example.com",
            "lastName": "Иванов",
            "firstName": "Иван",
            "middleName": "Иванович",
            "phoneNumber": "+79991234567"
        }
        
        logger.info(f"Создание пользователя с email: {user_request['email']}")
        response = client.create_user_api(user_request)
        response.raise_for_status()
        
        user_data = response.json()
        logger.info(f"Пользователь успешно создан: {user_data}")
        return user_data
        
    except Exception as e:
        logger.error(f"Ошибка при создании пользователя: {e}")
        raise


def open_credit_card_account(client, user_id: str) -> Dict[str, Any]:
    """
    Открытие кредитного счёта для пользователя.
    
    Args:
        client: Клиент для работы с API счетов
        user_id: Идентификатор пользователя
        
    Returns:
        Dict[str, Any]: Ответ от API с информацией о созданном счёте
    """
    try:
        from clients.http.gateway.accounts import OpenCreditCardAccountRequestDict
        
        # Подготовка данных для открытия кредитного счёта
        account_request: OpenCreditCardAccountRequestDict = {
            "userId": user_id,
            "currency": "RUB",
            "creditLimit": 50000.0,
            "interestRate": 15.5,
            "cardType": "PHYSICAL"
        }
        
        logger.info(f"Открытие кредитного счёта для пользователя: {user_id}")
        response = client.open_credit_card_account_api(account_request)
        response.raise_for_status()
        
        account_data = response.json()
        logger.info(f"Кредитный счёт успешно открыт: {account_data}")
        return account_data
        
    except Exception as e:
        logger.error(f"Ошибка при открытии кредитного счёта: {e}")
        raise


def get_tariff_document(client, account_id: str) -> Dict[str, Any]:
    """
    Получение документа тарифа для счёта.
    
    Args:
        client: Клиент для работы с API документов
        account_id: Идентификатор счёта
        
    Returns:
        Dict[str, Any]: Ответ от API с документом тарифа
    """
    try:
        logger.info(f"Получение документа тарифа для счёта: {account_id}")
        
        # Используем высокоуровневый метод
        tariff_document = client.get_tariff_document(account_id)
        logger.info(f"Документ тарифа получен: {tariff_document}")
        return tariff_document
        
    except Exception as e:
        logger.error(f"Ошибка при получении документа тарифа: {e}")
        raise


def get_contract_document(client, account_id: str) -> Dict[str, Any]:
    """
    Получение документа контракта для счёта.
    
    Args:
        client: Клиент для работы с API документов
        account_id: Идентификатор счёта
        
    Returns:
        Dict[str, Any]: Ответ от API с документом контракта
    """
    try:
        logger.info(f"Получение документа контракта для счёта: {account_id}")
        
        # Используем высокоуровневый метод
        contract_document = client.get_contract_document(account_id)
        logger.info(f"Документ контракта получен: {contract_document}")
        return contract_document
        
    except Exception as e:
        logger.error(f"Ошибка при получении документа контракта: {e}")
        raise


def main():
    """Основная функция скрипта."""
    try:
        logger.info("=" * 50)
        logger.info("НАЧАЛО РАБОТЫ СКРИПТА ПОЛУЧЕНИЯ ДОКУМЕНТОВ")
        logger.info("=" * 50)
        
        # 1. Создание клиентов
        logger.info("\n1. Создание API клиентов...")
        users_client = build_users_gateway_http_client()
        accounts_client = build_accounts_gateway_http_client()
        documents_client = build_documents_gateway_http_client()
        
        # 2. Создание пользователя
        logger.info("\n2. Создание пользователя...")
        user_response = create_user(users_client)
        user_id = user_response.get("user", {}).get("id")
        
        if not user_id:
            raise ValueError("Не удалось получить ID созданного пользователя")
        
        # 3. Открытие кредитного счёта
        logger.info("\n3. Открытие кредитного счёта...")
        account_response = open_credit_card_account(accounts_client, user_id)
        account_id = account_response.get("account", {}).get("id")
        
        if not account_id:
            raise ValueError("Не удалось получить ID созданного счёта")
        
        # 4. Получение документа тарифа
        logger.info("\n4. Получение документа тарифа...")
        tariff_response = get_tariff_document(documents_client, account_id)
        
        # 5. Получение документа контракта
        logger.info("\n5. Получение документа контракта...")
        contract_response = get_contract_document(documents_client, account_id)
        
        # Вывод итоговой информации
        logger.info("\n" + "=" * 50)
        logger.info("ИТОГОВЫЕ РЕЗУЛЬТАТЫ:")
        logger.info("=" * 50)
        logger.info(f"Create user response: {user_response}")
        logger.info(f"Open credit card account response: {account_response}")
        logger.info(f"Get tariff document response: {tariff_response}")
        logger.info(f"Get contract document response: {contract_response}")
        
        logger.info("\n✅ Все операции выполнены успешно!")
        
    except Exception as e:
        logger.error(f"❌ Ошибка выполнения скрипта: {e}")
        sys.exit(1)
    finally:
        logger.info("\n" + "=" * 50)
        logger.info("СКРИПТ ЗАВЕРШЁН")
        logger.info("=" * 50)


if __name__ == "__main__":
    main()
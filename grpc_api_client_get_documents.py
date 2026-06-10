from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.grpc.gateway.documents.client import build_documents_gateway_grpc_client
from clients.grpc.gateway.users.client import build_users_gateway_grpc_client


def main() -> None:
    """
    Основная функция скрипта.

    Выполняет последовательные шаги по созданию пользователя,
    открытию кредитного счёта и получению документов.
    """
    print("=" * 70)
    print("Скрипт получения документов по счёту (gRPC API-клиенты)")
    print("=" * 70)

    # Шаг 0: Создание API-клиентов для работы с сервисами
    print("\n0. Инициализация gRPC API-клиентов...")
    users_client = build_users_gateway_grpc_client()
    accounts_client = build_accounts_gateway_grpc_client()
    documents_client = build_documents_gateway_grpc_client()
    print("    Клиенты успешно созданы")

    # Шаг 1: Создание пользователя
    print("\n1. Создание нового пользователя...")
    create_user_response = users_client.create_user()
    print(f"Create user response: {create_user_response}")

    user_id = create_user_response.user.id
    print(f"    Пользователь создан. ID: {user_id}")
    print(f"   Email: {create_user_response.user.email}")
    print(f"   Имя: {create_user_response.user.first_name} {create_user_response.user.last_name}")

    # Шаг 2: Открытие кредитного счёта для пользователя
    print("\n2. Открытие кредитного счёта...")
    open_credit_card_account_response = accounts_client.open_credit_card_account(
        user_id=user_id
    )
    print(f"Open credit card account response: {open_credit_card_account_response}")

    account = open_credit_card_account_response.account
    account_id = account.id
    print(f"    Кредитный счёт открыт:")
    print(f"   - ID счёта: {account_id}")
    print(f"   - Тип счёта: {account.type}")
    print(f"   - Статус: {account.status}")
    print(f"   - Баланс: {account.balance}")

    # Выводим информацию о картах, созданных вместе со счётом
    print(f"   - Выпущенные карты:")
    for card in account.cards:
        print(f"     * {card.type}: ID={card.id}, номер={card.card_number}")

    # Шаг 3: Получение тарифного документа
    print("\n3. Получение тарифного документа...")
    get_tariff_document_response = documents_client.get_tariff_document(
        account_id=account_id
    )
    print(f"Get tariff document response: {get_tariff_document_response}")
    print(f"    Тарифный документ получен:")
    print(f"   - URL: {get_tariff_document_response.tariff.url}")
    print(f"   - Содержимое: {get_tariff_document_response.tariff.document}")

    # Шаг 4: Получение документа контракта
    print("\n4. Получение документа контракта...")
    get_contract_document_response = documents_client.get_contract_document(
        account_id=account_id
    )
    print(f"Get contract document response: {get_contract_document_response}")
    print(f"    Документ контракта получен:")
    print(f"   - URL: {get_contract_document_response.contract.url}")
    print(f"   - Содержимое: {get_contract_document_response.contract.document}")

    print("\n" + "=" * 70)
    print(" Скрипт успешно выполнен!")
    print("=" * 70)


if __name__ == "__main__":
    main()

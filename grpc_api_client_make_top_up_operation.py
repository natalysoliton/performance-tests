from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.grpc.gateway.operations.client import build_operations_gateway_grpc_client
from clients.grpc.gateway.users.client import build_users_gateway_grpc_client


def main() -> None:
    """
    Основная функция скрипта.

    Выполняет последовательные шаги по созданию пользователя,
    открытию дебетового счёта и созданию операции пополнения.
    """
    print("=" * 70)
    print("Скрипт создания операции пополнения счёта (gRPC API-клиенты)")
    print("=" * 70)

    # Шаг 0: Создание API-клиентов для работы с сервисами
    print("\n0. Инициализация gRPC API-клиентов...")
    users_client = build_users_gateway_grpc_client()
    accounts_client = build_accounts_gateway_grpc_client()
    operations_client = build_operations_gateway_grpc_client()
    print("    Клиенты успешно созданы")

    # Шаг 1: Создание пользователя
    print("\n1. Создание нового пользователя...")
    create_user_response = users_client.create_user()
    print(f"Create user response: {create_user_response}")

    user_id = create_user_response.user.id
    print(f"    Пользователь создан. ID: {user_id}")
    print(f"   Email: {create_user_response.user.email}")
    print(f"   Имя: {create_user_response.user.first_name} {create_user_response.user.last_name}")
    print(f"   Телефон: {create_user_response.user.phone_number}")

    # Шаг 2: Открытие дебетового счёта для пользователя
    print("\n2. Открытие дебетового счёта...")
    open_debit_card_account_response = accounts_client.open_debit_card_account(
        user_id=user_id
    )
    print(f"Open debit card account response: {open_debit_card_account_response}")

    account = open_debit_card_account_response.account
    account_id = account.id
    print(f"    Дебетовый счёт открыт:")
    print(f"   - ID счёта: {account_id}")
    print(f"   - Тип счёта: {account.type}")
    print(f"   - Статус: {account.status}")

    # Выводим информацию о картах, созданных вместе со счётом
    print(f"   - Выпущенные карты:")
    for i, card in enumerate(account.cards, 1):
        print(f"     Карта {i}:")
        print(f"       • ID: {card.id}")
        print(f"       • Тип: {card.type}")
        print(f"       • Номер: {card.card_number}")
        print(f"       • Держатель: {card.card_holder}")
        print(f"       • Статус: {card.status}")

    # Берём первую карту (виртуальную) для операции пополнения
    first_card_id = account.cards[0].id
    print(f"\n   - Для операции пополнения используется карта ID: {first_card_id}")

    # Шаг 3: Создание операции пополнения счёта
    print("\n3. Создание операции пополнения счёта...")
    make_top_up_operation_response = operations_client.make_top_up_operation(
        card_id=first_card_id,
        account_id=account_id
    )
    print(f"Make top up operation response: {make_top_up_operation_response}")

    operation = make_top_up_operation_response.operation
    print(f"    Операция пополнения создана:")
    print(f"   - ID операции: {operation.id}")
    print(f"   - Тип операции: {operation.type}")
    print(f"   - Статус: {operation.status}")
    print(f"   - Сумма: {operation.amount}")
    print(f"   - Категория: {operation.category}")
    print(f"   - Дата создания: {operation.created_at}")
    print(f"   - ID счёта: {operation.account_id}")
    print(f"   - ID карты: {operation.card_id}")

    print("\n" + "=" * 70)
    print(" Скрипт успешно выполнен!")
    print("=" * 70)


if __name__ == "__main__":
    main()

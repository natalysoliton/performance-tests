"""
Скрипт для тестирования операции пополнения счета через API.
Демонстрирует работу с вложенными списками и Pydantic-моделями,
включая доступ к данным счетов и карт через атрибуты.
"""

from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.operations.client import build_operations_gateway_http_client
from clients.http.gateway.users.client import build_users_gateway_http_client

# Инициализируем всех клиентов
users_gateway_client = build_users_gateway_http_client()
accounts_gateway_client = build_accounts_gateway_http_client()
operations_gateway_client = build_operations_gateway_http_client()

# Создаем пользователя
create_user_response = users_gateway_client.create_user()
print('Create user response:', create_user_response)
print(f"Создан пользователь: {create_user_response.user.first_name} {create_user_response.user.last_name}")
print(f"ID пользователя: {create_user_response.user.id}\n")

# Открываем дебетовый счет (используем атрибут .user.id)
open_debit_card_account_response = accounts_gateway_client.open_debit_card_account(
    user_id=create_user_response.user.id
)
print('Open debit card account response:', open_debit_card_account_response)
print(f"Открыт дебетовый счет ID: {open_debit_card_account_response.account.id}")
print(f"Баланс счета: {open_debit_card_account_response.account.balance}")
print(f"Тип счета: {open_debit_card_account_response.account.type}")
print(f"Статус счета: {open_debit_card_account_response.account.status}")
print(f"Количество карт на счете: {len(open_debit_card_account_response.account.cards)}\n")

# Получаем ID первой карты из списка (используем индексацию списка и атрибуты)
# Теперь обращаемся через атрибуты, а не через ключи словаря
if not open_debit_card_account_response.account.cards:
    raise RuntimeError("На счете нет карт для выполнения операции пополнения")

card_id = open_debit_card_account_response.account.cards[0].id
account_id = open_debit_card_account_response.account.id

print(f"📇 Информация о карте для пополнения:")
print(f"  ID карты: {card_id}")
print(f"  Статус карты: {open_debit_card_account_response.account.cards[0].status}")
print(f"  Тип карты: {open_debit_card_account_response.account.cards[0].type}")
print(f"  Платежная система: {open_debit_card_account_response.account.cards[0].payment_system}")
print(f"  Номер карты: {open_debit_card_account_response.account.cards[0].card_number}\n")

# Выполняем операцию пополнения
make_top_up_operation_response = operations_gateway_client.make_top_up_operation(
    card_id=card_id,
    account_id=account_id
)
print('Make top up operation response:', make_top_up_operation_response)

# Демонстрация доступа к данным ответа
print(f"\n💰 Результат операции пополнения:")
print(f"  Статус операции: {make_top_up_operation_response.status}")
print(f"  Сумма: {make_top_up_operation_response.amount} руб.")
print(f"  ID операции: {make_top_up_operation_response.operation_id}")
print(f"  Дата операции: {make_top_up_operation_response.created_at}")

# Дополнительная информация о счете после пополнения
print(f"\n📊 Итоговая информация по счету:")
print(f"  ID счета: {account_id}")
print(f"  Баланс до пополнения: {open_debit_card_account_response.account.balance} руб.")
print(f"  Баланс после пополнения: обновите счет для получения актуального баланса")
"""
Скрипт для тестирования выпуска физической карты через API.
Демонстрирует использование Pydantic-моделей для счетов и карт.
"""

from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.cards.client import build_cards_gateway_http_client
from clients.http.gateway.users.client import build_users_gateway_http_client

# Инициализируем всех клиентов
users_gateway_client = build_users_gateway_http_client()
cards_gateway_client = build_cards_gateway_http_client()
accounts_gateway_client = build_accounts_gateway_http_client()

# Создаем пользователя (возвращает Pydantic-модель)
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
print(f"Тип счета: {open_debit_card_account_response.account.type}")
print(f"Статус счета: {open_debit_card_account_response.account.status}")
print(f"Баланс счета: {open_debit_card_account_response.account.balance}\n")

# Выпускаем физическую карту
issue_physical_card_response = cards_gateway_client.issue_physical_card(
    user_id=create_user_response.user.id,
    account_id=open_debit_card_account_response.account.id
)
print('Issue physical card response:', issue_physical_card_response)

# Демонстрация доступа к данным выпущенной карты через атрибуты
print(f"\n📇 Детали выпущенной физической карты:")
print(f"  ID карты: {issue_physical_card_response.card.id}")
print(f"  Тип карты: {issue_physical_card_response.card.type}")
print(f"  Статус: {issue_physical_card_response.card.status}")
print(f"  Платежная система: {issue_physical_card_response.card.payment_system}")
print(f"  Номер карты: {issue_physical_card_response.card.card_number}")
print(f"  Владелец: {issue_physical_card_response.card.card_holder}")
print(f"  Срок действия: {issue_physical_card_response.card.expiry_date}")

# Проверяем, что карта добавилась в счет
print(f"\n📊 Обновленная информация о счете:")
print(f"  Баланс счета: {open_debit_card_account_response.account.balance}")
print(f"  Количество карт на счете: {len(open_debit_card_account_response.account.cards)}")
for i, card in enumerate(open_debit_card_account_response.account.cards, 1):
    print(f"    Карта {i}: {card.card_number} ({card.type})")
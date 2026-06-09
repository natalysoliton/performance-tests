"""
Скрипт для тестирования получения документов через API.
Демонстрирует использование Pydantic-моделей во всех клиентах,
включая работу со счетами и документами.
"""

from clients.http.gateway.accounts.client import build_accounts_gateway_http_client
from clients.http.gateway.documents.client import build_documents_gateway_http_client
from clients.http.gateway.users.client import build_users_gateway_http_client

# Инициализируем всех клиентов
users_gateway_client = build_users_gateway_http_client()
accounts_gateway_client = build_accounts_gateway_http_client()
documents_gateway_client = build_documents_gateway_http_client()

# Создаем пользователя (возвращает Pydantic-модель)
create_user_response = users_gateway_client.create_user()
print('Create user response:', create_user_response)
print(f" Создан пользователь: {create_user_response.user.first_name} {create_user_response.user.last_name}")
print(f"   ID пользователя: {create_user_response.user.id}")
print(f"   Email: {create_user_response.user.email}\n")

# Открываем кредитный счет (используем атрибут .user.id)
open_credit_card_account_response = accounts_gateway_client.open_credit_card_account(
    user_id=create_user_response.user.id
)
print('Open credit card account response:', open_credit_card_account_response)
print(f" Открыт кредитный счет:")
print(f"   ID счета: {open_credit_card_account_response.account.id}")
print(f"   Тип счета: {open_credit_card_account_response.account.type}")
print(f"   Статус счета: {open_credit_card_account_response.account.status}")
print(f"   Баланс счета: {open_credit_card_account_response.account.balance} руб.\n")

# Получаем тарифный документ (используем атрибут .account.id)
get_tariff_document_response = documents_gateway_client.get_tariff_document(
    account_id=open_credit_card_account_response.account.id
)
print('Get tariff document response:', get_tariff_document_response)
print(f"📄 Тарифный документ:")
print(f"   URL документа: {get_tariff_document_response.tariff.url}")
print(f"   Документ: {get_tariff_document_response.tariff.document}\n")

# Получаем контрактный документ
get_contract_document_response = documents_gateway_client.get_contract_document(
    account_id=open_credit_card_account_response.account.id
)
print('Get contract document response:', get_contract_document_response)
print(f" Контрактный документ:")
print(f"   URL документа: {get_contract_document_response.contract.url}")
print(f"   Документ: {get_contract_document_response.contract.document}\n")

# Демонстрация доступа к вложенным данным
print("Сводная информация:")
print(f"  Пользователь: {create_user_response.user.first_name} {create_user_response.user.last_name}")
print(f"  Email: {create_user_response.user.email}")
print(f"  Счет ID: {open_credit_card_account_response.account.id}")
print(f"  Баланс: {open_credit_card_account_response.account.balance} руб.")
print(f"  Карт на счете: {len(open_credit_card_account_response.account.cards)}")
print(f"  Тарифный документ: {get_tariff_document_response.tariff.url}")
print(f"  Контрактный документ: {get_contract_document_response.contract.url}")

# Если на счете есть карты, выводим информацию о первой
if open_credit_card_account_response.account.cards:
    first_card = open_credit_card_account_response.account.cards[0]
    print(f"\n💳 Информация о первой карте:")
    print(f"  Номер карты: {first_card.card_number}")
    print(f"  Тип карты: {first_card.type}")
    print(f"  Статус: {first_card.status}")
    print(f"  Платежная система: {first_card.payment_system}")
    print(f"  Срок действия: {first_card.expiry_date}")
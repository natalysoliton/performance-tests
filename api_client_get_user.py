"""
Скрипт для тестирования создания и получения пользователя через API.
Демонстрирует использование Pydantic-моделей вместо TypedDict.
"""

from clients.http.gateway.users.client import build_users_gateway_http_client

# Инициализируем клиент UsersGatewayHTTPClient
users_gateway_client = build_users_gateway_http_client()

# Создаем пользователя (метод возвращает Pydantic-модель)
create_user_response = users_gateway_client.create_user()
print('Create user data:', create_user_response)

# Получаем данные пользователя по ID (используем атрибут .user.id вместо словаря)
get_user_response = users_gateway_client.get_user(create_user_response.user.id)
print('Get user data:', get_user_response)

# Демонстрация доступа к данным через атрибуты
print(f"\nДетали созданного пользователя:")
print(f"  ID: {create_user_response.user.id}")
print(f"  Email: {create_user_response.user.email}")
print(f"  Имя: {create_user_response.user.first_name}")
print(f"  Фамилия: {create_user_response.user.last_name}")
print(f"  Отчество: {create_user_response.user.middle_name}")
print(f"  Телефон: {create_user_response.user.phone_number}")
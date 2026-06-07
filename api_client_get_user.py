import time

from clients.http.gateway.users.client import (
    CreateUserRequestDict,
    build_users_gateway_http_client
)

# Инициализируем клиент UsersGatewayHTTPClient
users_gateway_client = build_users_gateway_http_client()

# Инициализируем запрос на создание пользователя
create_user_request = CreateUserRequestDict(
    email=f"user.{time.time()}@example.com",
    lastName="string",
    firstName="string",
    middleName="string",
    phoneNumber="string"
)
# Отправляем POST запрос на создание пользователя
create_user_response = users_gateway_client.create_user_api(create_user_request)
create_user_response_data = create_user_response.json()
print('Create user data:', create_user_response_data)

# Отправляем GET запрос на получение данных пользователя
get_user_response = users_gateway_client.get_user_api(create_user_response_data['user']['id'])
get_user_response_data = get_user_response.json()
print('Get user data:', get_user_response_data)

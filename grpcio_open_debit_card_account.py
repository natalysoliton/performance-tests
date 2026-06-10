import grpc
from typing import Tuple

# Импорт сгенерированных контрактов для UsersGatewayService
from contracts.services.gateway.users.rpc_create_user_pb2 import (
    CreateUserRequest,
    CreateUserResponse
)
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import (
    UsersGatewayServiceStub
)

# Импорт сгенерированных контрактов для AccountsGatewayService
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import (
    OpenDebitCardAccountRequest,
    OpenDebitCardAccountResponse
)
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import (
    AccountsGatewayServiceStub
)

# Импорт генератора фейковых данных
from tools.fakers import fake


def create_user(stub: UsersGatewayServiceStub) -> CreateUserResponse:
    """
    Создание нового пользователя с рандомными данными.

    Args:
        stub: gRPC клиент для UsersGatewayService

    Returns:
        CreateUserResponse: Ответ сервера с данными созданного пользователя
    """
    # Формируем запрос с фейковыми данными пользователя
    create_user_request = CreateUserRequest(
        email=fake.email(),
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        middle_name=fake.middle_name(),
        phone_number=fake.phone_number()
    )

    # Отправляем запрос и получаем ответ
    response: CreateUserResponse = stub.CreateUser(create_user_request)
    return response


def open_debit_card_account(
        stub: AccountsGatewayServiceStub,
        user_id: str
) -> OpenDebitCardAccountResponse:
    """
    Открытие дебетового аккаунта для указанного пользователя.

    Args:
        stub: gRPC клиент для AccountsGatewayService
        user_id: Идентификатор пользователя, для которого открывается аккаунт

    Returns:
        OpenDebitCardAccountResponse: Ответ сервера с данными аккаунта и карт
    """
    # Формируем запрос на открытие дебетового аккаунта
    open_account_request = OpenDebitCardAccountRequest(
        user_id=user_id
    )

    # Отправляем запрос и получаем ответ
    response: OpenDebitCardAccountResponse = stub.OpenDebitCardAccount(open_account_request)
    return response


def print_results(
        create_user_response: CreateUserResponse,
        account_response: OpenDebitCardAccountResponse
) -> None:
    """
    Вывод результатов в требуемом формате.

    Args:
        create_user_response: Ответ с данными пользователя
        account_response: Ответ с данными аккаунта и карт
    """
    print("Create user response:", create_user_response)
    print("Open debit card account response:", account_response)


def main() -> None:
    """
    Основная функция скрипта.

    Выполняет последовательные шаги:
    1. Устанавливает соединение с gRPC-сервером
    2. Создает пользователя
    3. Открывает дебетовый аккаунт для созданного пользователя
    4. Выводит результаты
    """
    # Адрес gRPC-шлюза
    GRPC_GATEWAY_ADDRESS = "localhost:9003"

    print(f"Подключение к gRPC-серверу по адресу: {GRPC_GATEWAY_ADDRESS}")

    # Устанавливаем соединение с gRPC-сервером
    channel = grpc.insecure_channel(GRPC_GATEWAY_ADDRESS)

    # Создаём gRPC-клиенты для логических сервисов
    users_service: UsersGatewayServiceStub = UsersGatewayServiceStub(channel)
    accounts_service: AccountsGatewayServiceStub = AccountsGatewayServiceStub(channel)

    print("=" * 60)

    # Шаг 1: Создание пользователя
    print("Шаг 1: Создание нового пользователя...")
    create_user_response: CreateUserResponse = create_user(users_service)
    user_id: str = create_user_response.user.id
    print(f"Пользователь успешно создан. ID: {user_id}")

    print("-" * 60)

    # Шаг 2: Открытие дебетового аккаунта
    print(f"Шаг 2: Открытие дебетового аккаунта для пользователя {user_id}...")
    account_response: OpenDebitCardAccountResponse = open_debit_card_account(
        accounts_service,
        user_id
    )
    print("Дебетовый аккаунт успешно открыт.")

    print("-" * 60)

    # Шаг 3: Вывод результатов
    print("Результаты выполнения:")
    print_results(create_user_response, account_response)

    print("=" * 60)
    print("Скрипт успешно завершён.")


if __name__ == "__main__":
    main()

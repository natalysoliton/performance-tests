import grpc

# Импорты для работы с пользователями
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub

# Импорты для работы с дебетовым счётом
from contracts.services.gateway.accounts.accounts_gateway_service_pb2_grpc import AccountsGatewayServiceStub
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import (
    OpenDebitCardAccountRequest,
    OpenDebitCardAccountResponse
)

# Импорты для работы с операциями
from contracts.services.gateway.operations.operations_gateway_service_pb2_grpc import OperationsGatewayServiceStub
from contracts.services.gateway.operations.rpc_make_top_up_operation_pb2 import (
    MakeTopUpOperationRequest,
    MakeTopUpOperationResponse
)
from contracts.services.gateway.operations.rpc_get_operation_receipt_pb2 import (
    GetOperationReceiptRequest,
    GetOperationReceiptResponse
)

# Импорт статусов операций
from contracts.services.operations.operation_pb2 import OperationStatus

# Импорт генератора фейковых данных
from tools.fakers import fake


def create_user(stub: UsersGatewayServiceStub) -> CreateUserResponse:
    """
    Создание нового пользователя с фейковыми данными.

    Args:
        stub: gRPC клиент для UsersGatewayService

    Returns:
        CreateUserResponse: Данные созданного пользователя
    """
    create_user_request = CreateUserRequest(
        email=fake.email(),
        last_name=fake.last_name(),
        first_name=fake.first_name(),
        middle_name=fake.middle_name(),
        phone_number=fake.phone_number()
    )

    response: CreateUserResponse = stub.CreateUser(create_user_request)
    print('Create user response:', response)
    return response


def open_debit_card_account(stub: AccountsGatewayServiceStub, user_id: str) -> OpenDebitCardAccountResponse:
    """
    Открытие дебетового счёта для пользователя.

    Args:
        stub: gRPC клиент для AccountsGatewayService
        user_id: Идентификатор пользователя

    Returns:
        OpenDebitCardAccountResponse: Данные открытого счёта и карт
    """
    open_account_request = OpenDebitCardAccountRequest(user_id=user_id)

    response: OpenDebitCardAccountResponse = stub.OpenDebitCardAccount(open_account_request)
    print('Open debit card account response:', response)
    return response


def make_top_up_operation(
        stub: OperationsGatewayServiceStub,
        account_id: str,
        card_id: str,
        amount: float
) -> MakeTopUpOperationResponse:
    """
    Выполнение операции пополнения счёта.

    Args:
        stub: gRPC клиент для OperationsGatewayService
        account_id: Идентификатор счёта
        card_id: Идентификатор карты
        amount: Сумма пополнения

    Returns:
        MakeTopUpOperationResponse: Данные об операции пополнения
    """
    top_up_request = MakeTopUpOperationRequest(
        status=OperationStatus.OPERATION_STATUS_COMPLETED,  # Статус "Завершено"
        amount=amount,
        card_id=card_id,
        account_id=account_id
    )

    response: MakeTopUpOperationResponse = stub.MakeTopUpOperation(top_up_request)
    print('Make top up operation response:', response)
    return response


def get_operation_receipt(
        stub: OperationsGatewayServiceStub,
        operation_id: str
) -> GetOperationReceiptResponse:
    """
    Получение чека по операции.

    Args:
        stub: gRPC клиент для OperationsGatewayService
        operation_id: Идентификатор операции

    Returns:
        GetOperationReceiptResponse: Данные чека (URL и документ)
    """
    receipt_request = GetOperationReceiptRequest(operation_id=operation_id)

    response: GetOperationReceiptResponse = stub.GetOperationReceipt(receipt_request)

    # Выводим в требуемом формате
    print(f'Get operation receipt response: receipt {{\n'
          f'  url: "{response.receipt.url}"\n'
          f'  document: "{response.receipt.document}"\n'
          f'}}')

    return response


def main() -> None:
    """
    Основная функция скрипта.

    Выполняет последовательные шаги:
    1. Устанавливает соединение с gRPC-шлюзом
    2. Создаёт пользователя
    3. Открывает дебетовый счёт
    4. Пополняет счёт
    5. Получает и выводит чек по операции
    """
    # Адрес gRPC-шлюза
    GRPC_GATEWAY_ADDRESS = "localhost:9003"

    print(f"Подключение к gRPC-серверу по адресу: {GRPC_GATEWAY_ADDRESS}")
    print("=" * 60)

    # Устанавливаем соединение с gRPC-сервером
    channel = grpc.insecure_channel(GRPC_GATEWAY_ADDRESS)

    # Инициализируем gRPC-клиентов для всех необходимых сервисов
    users_stub = UsersGatewayServiceStub(channel)
    accounts_stub = AccountsGatewayServiceStub(channel)
    operations_stub = OperationsGatewayServiceStub(channel)

    # Шаг 1: Создание пользователя
    print("Шаг 1: Создание нового пользователя...")
    user_response = create_user(users_stub)
    user_id = user_response.user.id
    print(f"✓ Пользователь создан. ID: {user_id}")
    print("-" * 60)

    # Шаг 2: Открытие дебетового счёта
    print(f"Шаг 2: Открытие дебетового счёта для пользователя {user_id}...")
    account_response = open_debit_card_account(accounts_stub, user_id)
    account_id = account_response.account.id
    # Берём первую карту (виртуальную) из ответа
    card_id = account_response.account.cards[0].id
    print(f"✓ Дебетовый счёт открыт. ID счёта: {account_id}, ID карты: {card_id}")
    print("-" * 60)

    # Шаг 3: Пополнение счёта
    print("Шаг 3: Выполнение операции пополнения счёта...")
    amount = fake.amount()  # Генерируем случайную сумму пополнения
    print(f"Сумма пополнения: {amount}")

    operation_response = make_top_up_operation(
        stub=operations_stub,
        account_id=account_id,
        card_id=card_id,
        amount=amount
    )
    operation_id = operation_response.operation.id
    print(f"✓ Операция пополнения выполнена. ID операции: {operation_id}")
    print("-" * 60)

    # Шаг 4: Получение чека по операции
    print(f"Шаг 4: Получение чека по операции {operation_id}...")
    get_operation_receipt(operations_stub, operation_id)
    print("✓ Чек успешно получен")

    print("=" * 60)
    print("Скрипт успешно завершён.")


if __name__ == "__main__":
    main()

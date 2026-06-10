from grpc import Channel

from clients.grpc.client import GRPCClient
from clients.grpc.gateway.client import build_gateway_grpc_client
from contracts.services.gateway.operations.operations_gateway_service_pb2_grpc import (
    OperationsGatewayServiceStub
)
from contracts.services.gateway.operations.rpc_get_operation_pb2 import (
    GetOperationRequest,
    GetOperationResponse
)
from contracts.services.gateway.operations.rpc_get_operation_receipt_pb2 import (
    GetOperationReceiptRequest,
    GetOperationReceiptResponse
)
from contracts.services.gateway.operations.rpc_get_operations_pb2 import (
    GetOperationsRequest,
    GetOperationsResponse
)
from contracts.services.gateway.operations.rpc_get_operations_summary_pb2 import (
    GetOperationsSummaryRequest,
    GetOperationsSummaryResponse
)
from contracts.services.gateway.operations.rpc_make_fee_operation_pb2 import (
    MakeFeeOperationRequest,
    MakeFeeOperationResponse
)
from contracts.services.gateway.operations.rpc_make_top_up_operation_pb2 import (
    MakeTopUpOperationRequest,
    MakeTopUpOperationResponse
)
from contracts.services.gateway.operations.rpc_make_cashback_operation_pb2 import (
    MakeCashbackOperationRequest,
    MakeCashbackOperationResponse
)
from contracts.services.gateway.operations.rpc_make_transfer_operation_pb2 import (
    MakeTransferOperationRequest,
    MakeTransferOperationResponse
)
from contracts.services.gateway.operations.rpc_make_purchase_operation_pb2 import (
    MakePurchaseOperationRequest,
    MakePurchaseOperationResponse
)
from contracts.services.gateway.operations.rpc_make_bill_payment_operation_pb2 import (
    MakeBillPaymentOperationRequest,
    MakeBillPaymentOperationResponse
)
from contracts.services.gateway.operations.rpc_make_cash_withdrawal_operation_pb2 import (
    MakeCashWithdrawalOperationRequest,
    MakeCashWithdrawalOperationResponse
)
from contracts.services.operations.operation_pb2 import OperationStatus
from tools.fakers import fake


class OperationsGatewayGRPCClient(GRPCClient):
    """
    gRPC-клиент для взаимодействия с OperationsGatewayService.

    Предоставляет методы для работы с банковскими операциями:
    - Просмотр операций по счету
    - Получение чеков
    - Создание различных типов операций

    Examples:
        >>> client = build_operations_gateway_grpc_client()
        >>>
        >>> # Получение информации об операции
        >>> operation = client.get_operation(operation_id="123e4567-...")
        >>>
        >>> # Создание операции покупки
        >>> purchase = client.make_purchase_operation(
        ...     card_id="card-123",
        ...     account_id="account-456"
        ... )
    """

    def __init__(self, channel: Channel):
        """
        Инициализация клиента для OperationsGatewayService.

        Args:
            channel: gRPC-канал для подключения к сервису
        """
        super().__init__(channel)

        # gRPC-стаб, сгенерированный из .proto файла
        self._stub = OperationsGatewayServiceStub(channel)

    # ==================== Низкоуровневые API-методы ====================

    def get_operation_api(self, request: GetOperationRequest) -> GetOperationResponse:
        """
        Низкоуровневый вызов метода GetOperation через gRPC.

        Получение информации об операции по её идентификатору.

        Args:
            request: GetOperationRequest с ID операции

        Returns:
            GetOperationResponse с данными об операции

        Example:
            >>> request = GetOperationRequest(operation_id="123e4567-...")
            >>> response = client.get_operation_api(request)
        """
        return self._stub.GetOperation(request)

    def get_operation_receipt_api(
            self,
            request: GetOperationReceiptRequest
    ) -> GetOperationReceiptResponse:
        """
        Низкоуровневый вызов метода GetOperationReceipt через gRPC.

        Получение чека по операции.

        Args:
            request: GetOperationReceiptRequest с ID операции

        Returns:
            GetOperationReceiptResponse с данными чека (URL и содержимое)

        Example:
            >>> request = GetOperationReceiptRequest(operation_id="123e4567-...")
            >>> response = client.get_operation_receipt_api(request)
        """
        return self._stub.GetOperationReceipt(request)

    def get_operations_api(self, request: GetOperationsRequest) -> GetOperationsResponse:
        """
        Низкоуровневый вызов метода GetOperations через gRPC.

        Получение списка всех операций для указанного счёта.

        Args:
            request: GetOperationsRequest с ID счёта

        Returns:
            GetOperationsResponse со списком операций

        Example:
            >>> request = GetOperationsRequest(account_id="account-456")
            >>> response = client.get_operations_api(request)
        """
        return self._stub.GetOperations(request)

    def get_operations_summary_api(
            self,
            request: GetOperationsSummaryRequest
    ) -> GetOperationsSummaryResponse:
        """
        Низкоуровневый вызов метода GetOperationsSummary через gRPC.

        Получение статистики по операциям для указанного счёта.

        Args:
            request: GetOperationsSummaryRequest с ID счёта

        Returns:
            GetOperationsSummaryResponse со статистикой операций

        Example:
            >>> request = GetOperationsSummaryRequest(account_id="account-456")
            >>> response = client.get_operations_summary_api(request)
        """
        return self._stub.GetOperationsSummary(request)

    def make_fee_operation_api(
            self,
            request: MakeFeeOperationRequest
    ) -> MakeFeeOperationResponse:
        """
        Низкоуровневый вызов метода MakeFeeOperation через gRPC.

        Создание операции комиссии.

        Args:
            request: MakeFeeOperationRequest с данными для создания комиссии

        Returns:
            MakeFeeOperationResponse с данными созданной операции

        Example:
            >>> request = MakeFeeOperationRequest(
            ...     status=OperationStatus.OPERATION_STATUS_COMPLETED,
            ...     amount=100.00,
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
            >>> response = client.make_fee_operation_api(request)
        """
        return self._stub.MakeFeeOperation(request)

    def make_top_up_operation_api(
            self,
            request: MakeTopUpOperationRequest
    ) -> MakeTopUpOperationResponse:
        """
        Низкоуровневый вызов метода MakeTopUpOperation через gRPC.

        Создание операции пополнения счёта.

        Args:
            request: MakeTopUpOperationRequest с данными для пополнения

        Returns:
            MakeTopUpOperationResponse с данными созданной операции

        Example:
            >>> request = MakeTopUpOperationRequest(
            ...     status=OperationStatus.OPERATION_STATUS_COMPLETED,
            ...     amount=500.00,
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
            >>> response = client.make_top_up_operation_api(request)
        """
        return self._stub.MakeTopUpOperation(request)

    def make_cashback_operation_api(
            self,
            request: MakeCashbackOperationRequest
    ) -> MakeCashbackOperationResponse:
        """
        Низкоуровневый вызов метода MakeCashbackOperation через gRPC.

        Создание операции кэшбэка.

        Args:
            request: MakeCashbackOperationRequest с данными для кэшбэка

        Returns:
            MakeCashbackOperationResponse с данными созданной операции

        Example:
            >>> request = MakeCashbackOperationRequest(
            ...     status=OperationStatus.OPERATION_STATUS_COMPLETED,
            ...     amount=50.00,
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
            >>> response = client.make_cashback_operation_api(request)
        """
        return self._stub.MakeCashbackOperation(request)

    def make_transfer_operation_api(
            self,
            request: MakeTransferOperationRequest
    ) -> MakeTransferOperationResponse:
        """
        Низкоуровневый вызов метода MakeTransferOperation через gRPC.

        Создание операции перевода средств.

        Args:
            request: MakeTransferOperationRequest с данными для перевода

        Returns:
            MakeTransferOperationResponse с данными созданной операции

        Example:
            >>> request = MakeTransferOperationRequest(
            ...     status=OperationStatus.OPERATION_STATUS_COMPLETED,
            ...     amount=200.00,
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
            >>> response = client.make_transfer_operation_api(request)
        """
        return self._stub.MakeTransferOperation(request)

    def make_purchase_operation_api(
            self,
            request: MakePurchaseOperationRequest
    ) -> MakePurchaseOperationResponse:
        """
        Низкоуровневый вызов метода MakePurchaseOperation через gRPC.

        Создание операции покупки.

        Args:
            request: MakePurchaseOperationRequest с данными для покупки

        Returns:
            MakePurchaseOperationResponse с данными созданной операции

        Example:
            >>> request = MakePurchaseOperationRequest(
            ...     status=OperationStatus.OPERATION_STATUS_COMPLETED,
            ...     amount=150.00,
            ...     card_id="card-123",
            ...     category="restaurant",
            ...     account_id="account-456"
            ... )
            >>> response = client.make_purchase_operation_api(request)
        """
        return self._stub.MakePurchaseOperation(request)

    def make_bill_payment_operation_api(
            self,
            request: MakeBillPaymentOperationRequest
    ) -> MakeBillPaymentOperationResponse:
        """
        Низкоуровневый вызов метода MakeBillPaymentOperation через gRPC.

        Создание операции оплаты счёта.

        Args:
            request: MakeBillPaymentOperationRequest с данными для оплаты

        Returns:
            MakeBillPaymentOperationResponse с данными созданной операции

        Example:
            >>> request = MakeBillPaymentOperationRequest(
            ...     status=OperationStatus.OPERATION_STATUS_COMPLETED,
            ...     amount=300.00,
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
            >>> response = client.make_bill_payment_operation_api(request)
        """
        return self._stub.MakeBillPaymentOperation(request)

    def make_cash_withdrawal_operation_api(
            self,
            request: MakeCashWithdrawalOperationRequest
    ) -> MakeCashWithdrawalOperationResponse:
        """
        Низкоуровневый вызов метода MakeCashWithdrawalOperation через gRPC.

        Создание операции снятия наличных.

        Args:
            request: MakeCashWithdrawalOperationRequest с данными для снятия

        Returns:
            MakeCashWithdrawalOperationResponse с данными созданной операции

        Example:
            >>> request = MakeCashWithdrawalOperationRequest(
            ...     status=OperationStatus.OPERATION_STATUS_COMPLETED,
            ...     amount=100.00,
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
            >>> response = client.make_cash_withdrawal_operation_api(request)
        """
        return self._stub.MakeCashWithdrawalOperation(request)

    # ==================== Высокоуровневые методы-обёртки ====================

    def get_operation(self, operation_id: str) -> GetOperationResponse:
        """
        Получение информации об операции по её ID.

        Args:
            operation_id: Идентификатор операции (UUID)

        Returns:
            GetOperationResponse с данными об операции

        Example:
            >>> response = client.get_operation("123e4567-e89b-12d3-a456-426614174000")
            >>> print(f"Тип операции: {response.operation.type}")
            >>> print(f"Сумма: {response.operation.amount}")
        """
        request = GetOperationRequest(operation_id=operation_id)
        return self.get_operation_api(request)

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponse:
        """
        Получение чека по операции.

        Args:
            operation_id: Идентификатор операции (UUID)

        Returns:
            GetOperationReceiptResponse с данными чека

        Example:
            >>> response = client.get_operation_receipt("123e4567-e89b-12d3-a456-426614174000")
            >>> print(f"URL чека: {response.receipt.url}")
            >>> print(f"Содержимое: {response.receipt.document}")
        """
        request = GetOperationReceiptRequest(operation_id=operation_id)
        return self.get_operation_receipt_api(request)

    def get_operations(self, account_id: str) -> GetOperationsResponse:
        """
        Получение списка всех операций для указанного счёта.

        Args:
            account_id: Идентификатор счёта (UUID)

        Returns:
            GetOperationsResponse со списком операций

        Example:
            >>> response = client.get_operations("account-456")
            >>> for op in response.operations:
            ...     print(f"{op.type}: {op.amount}")
        """
        request = GetOperationsRequest(account_id=account_id)
        return self.get_operations_api(request)

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponse:
        """
        Получение статистики по операциям для указанного счёта.

        Args:
            account_id: Идентификатор счёта (UUID)

        Returns:
            GetOperationsSummaryResponse со статистикой операций

        Example:
            >>> response = client.get_operations_summary("account-456")
            >>> print(f"Всего операций: {response.total_count}")
            >>> print(f"Общая сумма: {response.total_amount}")
        """
        request = GetOperationsSummaryRequest(account_id=account_id)
        return self.get_operations_summary_api(request)

    def make_fee_operation(
            self,
            card_id: str,
            account_id: str
    ) -> MakeFeeOperationResponse:
        """
        Создание операции комиссии с автоматически сгенерированными данными.

        Args:
            card_id: Идентификатор карты
            account_id: Идентификатор счёта

        Returns:
            MakeFeeOperationResponse с данными созданной операции

        Example:
            >>> response = client.make_fee_operation(
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
            >>> print(f"Операция создана: {response.operation.id}")
        """
        request = MakeFeeOperationRequest(
            status=fake.proto_enum(OperationStatus),
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_fee_operation_api(request)

    def make_top_up_operation(
            self,
            card_id: str,
            account_id: str
    ) -> MakeTopUpOperationResponse:
        """
        Создание операции пополнения счёта с автоматически сгенерированными данными.

        Args:
            card_id: Идентификатор карты
            account_id: Идентификатор счёта

        Returns:
            MakeTopUpOperationResponse с данными созданной операции

        Example:
            >>> response = client.make_top_up_operation(
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
            >>> print(f"Пополнение на сумму: {response.operation.amount}")
        """
        request = MakeTopUpOperationRequest(
            status=fake.proto_enum(OperationStatus),
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_top_up_operation_api(request)

    def make_cashback_operation(
            self,
            card_id: str,
            account_id: str
    ) -> MakeCashbackOperationResponse:
        """
        Создание операции кэшбэка с автоматически сгенерированными данными.

        Args:
            card_id: Идентификатор карты
            account_id: Идентификатор счёта

        Returns:
            MakeCashbackOperationResponse с данными созданной операции

        Example:
            >>> response = client.make_cashback_operation(
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
        """
        request = MakeCashbackOperationRequest(
            status=fake.proto_enum(OperationStatus),
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_cashback_operation_api(request)

    def make_transfer_operation(
            self,
            card_id: str,
            account_id: str
    ) -> MakeTransferOperationResponse:
        """
        Создание операции перевода с автоматически сгенерированными данными.

        Args:
            card_id: Идентификатор карты
            account_id: Идентификатор счёта

        Returns:
            MakeTransferOperationResponse с данными созданной операции

        Example:
            >>> response = client.make_transfer_operation(
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
        """
        request = MakeTransferOperationRequest(
            status=fake.proto_enum(OperationStatus),
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_transfer_operation_api(request)

    def make_purchase_operation(
            self,
            card_id: str,
            account_id: str
    ) -> MakePurchaseOperationResponse:
        """
        Создание операции покупки с автоматически сгенерированными данными.

        Args:
            card_id: Идентификатор карты
            account_id: Идентификатор счёта

        Returns:
            MakePurchaseOperationResponse с данными созданной операции

        Example:
            >>> response = client.make_purchase_operation(
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
            >>> print(f"Категория покупки: {response.operation.category}")
        """
        request = MakePurchaseOperationRequest(
            status=fake.proto_enum(OperationStatus),
            amount=fake.amount(),
            card_id=card_id,
            category=fake.category(),
            account_id=account_id
        )
        return self.make_purchase_operation_api(request)

    def make_bill_payment_operation(
            self,
            card_id: str,
            account_id: str
    ) -> MakeBillPaymentOperationResponse:
        """
        Создание операции оплаты счёта с автоматически сгенерированными данными.

        Args:
            card_id: Идентификатор карты
            account_id: Идентификатор счёта

        Returns:
            MakeBillPaymentOperationResponse с данными созданной операции

        Example:
            >>> response = client.make_bill_payment_operation(
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
        """
        request = MakeBillPaymentOperationRequest(
            status=fake.proto_enum(OperationStatus),
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_bill_payment_operation_api(request)

    def make_cash_withdrawal_operation(
            self,
            card_id: str,
            account_id: str
    ) -> MakeCashWithdrawalOperationResponse:
        """
        Создание операции снятия наличных с автоматически сгенерированными данными.

        Args:
            card_id: Идентификатор карты
            account_id: Идентификатор счёта

        Returns:
            MakeCashWithdrawalOperationResponse с данными созданной операции

        Example:
            >>> response = client.make_cash_withdrawal_operation(
            ...     card_id="card-123",
            ...     account_id="account-456"
            ... )
        """
        request = MakeCashWithdrawalOperationRequest(
            status=fake.proto_enum(OperationStatus),
            amount=fake.amount(),
            card_id=card_id,
            account_id=account_id
        )
        return self.make_cash_withdrawal_operation_api(request)


# ==================== Фабричная функция (Билдер) ====================

def build_operations_gateway_grpc_client() -> OperationsGatewayGRPCClient:
    """
    Фабричная функция для создания экземпляра OperationsGatewayGRPCClient.

    Скрывает детали создания gRPC-канала и инициализации клиента.

    Returns:
        OperationsGatewayGRPCClient: Инициализированный клиент для OperationsGatewayService

    Example:
        >>> client = build_operations_gateway_grpc_client()
        >>> purchase = client.make_purchase_operation("card-123", "account-456")
    """
    channel = build_gateway_grpc_client()
    return OperationsGatewayGRPCClient(channel=channel)

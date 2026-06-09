"""
HTTP-клиент для взаимодействия с /api/v1/operations сервиса http-gateway.
Использует Pydantic-модели для валидации запросов и ответов.
Теперь все поля (status, amount, category) генерируются автоматически на уровне моделей.
"""

from httpx import Response, QueryParams

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.operations.schema import (
    # Enum-ы
    OperationStatus,
    # Модели запросов
    GetOperationsQuerySchema,
    GetOperationsSummaryQuerySchema,
    MakeFeeOperationRequestSchema,
    MakeTopUpOperationRequestSchema,
    MakeCashbackOperationRequestSchema,
    MakeTransferOperationRequestSchema,
    MakePurchaseOperationRequestSchema,
    MakeBillPaymentOperationRequestSchema,
    MakeCashWithdrawalOperationRequestSchema,
    # Модели ответов
    GetOperationResponseSchema,
    GetOperationReceiptResponseSchema,
    GetOperationsResponseSchema,
    GetOperationsSummaryResponseSchema,
    MakeFeeOperationResponseSchema,
    MakeTopUpOperationResponseSchema,
    MakeCashbackOperationResponseSchema,
    MakeTransferOperationResponseSchema,
    MakePurchaseOperationResponseSchema,
    MakeBillPaymentOperationResponseSchema,
    MakeCashWithdrawalOperationResponseSchema,
)


class OperationsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/operations сервиса http-gateway.

    Предоставляет методы для работы с операциями:
    - Получение информации об операции
    - Получение чека по операции
    - Получение списка операций по счету
    - Получение статистики по операциям
    - Создание различных типов операций (комиссия, пополнение, кэшбэк,
      перевод, покупка, оплата счета, снятие наличных)
    """

    def get_operation_api(self, operation_id: str) -> Response:
        """
        Получает информацию об операции по её идентификатору.

        :param operation_id: Уникальный идентификатор операции.
        :return: Объект httpx.Response с данными об операции.
        """
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """
        Получает чек по заданной операции.

        :param operation_id: Уникальный идентификатор операции.
        :return: Объект httpx.Response с чеком по операции.
        """
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQuerySchema) -> Response:
        """
        Получает список операций по счёту.

        :param query: Pydantic-модель с параметром accountId.
        :return: Объект httpx.Response с операциями по счёту.
        """
        return self.get(
            "/api/v1/operations",
            params=QueryParams(**query.model_dump(by_alias=True))
        )

    def get_operations_summary_api(self, query: GetOperationsSummaryQuerySchema) -> Response:
        """
        Получает сводную статистику операций по счёту.

        :param query: Pydantic-модель с параметром accountId.
        :return: Объект httpx.Response с агрегированной информацией.
        """
        return self.get(
            "/api/v1/operations/operations-summary",
            params=QueryParams(**query.model_dump(by_alias=True))
        )

    def make_fee_operation_api(self, request: MakeFeeOperationRequestSchema) -> Response:
        """
        Создаёт операцию комиссии.

        :param request: Pydantic-модель с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(
            "/api/v1/operations/make-fee-operation",
            json=request.model_dump(by_alias=True)
        )

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestSchema) -> Response:
        """
        Создаёт операцию пополнения счёта.

        :param request: Pydantic-модель с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(
            "/api/v1/operations/make-top-up-operation",
            json=request.model_dump(by_alias=True)
        )

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestSchema) -> Response:
        """
        Создаёт операцию начисления кэшбэка.

        :param request: Pydantic-модель с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(
            "/api/v1/operations/make-cashback-operation",
            json=request.model_dump(by_alias=True)
        )

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestSchema) -> Response:
        """
        Создаёт операцию перевода средств.

        :param request: Pydantic-модель с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(
            "/api/v1/operations/make-transfer-operation",
            json=request.model_dump(by_alias=True)
        )

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestSchema) -> Response:
        """
        Создаёт операцию покупки.

        :param request: Pydantic-модель с параметрами операции, включая категорию.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(
            "/api/v1/operations/make-purchase-operation",
            json=request.model_dump(by_alias=True)
        )

    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequestSchema) -> Response:
        """
        Создаёт операцию оплаты счёта.

        :param request: Pydantic-модель с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(
            "/api/v1/operations/make-bill-payment-operation",
            json=request.model_dump(by_alias=True)
        )

    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequestSchema) -> Response:
        """
        Создаёт операцию снятия наличных средств.

        :param request: Pydantic-модель с параметрами операции.
        :return: Объект httpx.Response с результатом операции.
        """
        return self.post(
            "/api/v1/operations/make-cash-withdrawal-operation",
            json=request.model_dump(by_alias=True)
        )

    def get_operation(self, operation_id: str) -> GetOperationResponseSchema:
        """
        Получает информацию об операции и возвращает как Pydantic-модель.

        :param operation_id: Уникальный идентификатор операции.
        :return: Pydantic-модель с данными об операции.
        """
        response = self.get_operation_api(operation_id)
        return GetOperationResponseSchema.model_validate_json(response.text)

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseSchema:
        """
        Получает чек по операции и возвращает как Pydantic-модель.

        :param operation_id: Уникальный идентификатор операции.
        :return: Pydantic-модель с чеком операции.
        """
        response = self.get_operation_receipt_api(operation_id)
        return GetOperationReceiptResponseSchema.model_validate_json(response.text)

    def get_operations(self, account_id: str) -> GetOperationsResponseSchema:
        """
        Получает список операций по счету и возвращает как Pydantic-модель.

        :param account_id: ID счета для фильтрации операций.
        :return: Pydantic-модель со списком операций.
        """
        query = GetOperationsQuerySchema(account_id=account_id)
        response = self.get_operations_api(query)
        return GetOperationsResponseSchema.model_validate_json(response.text)

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseSchema:
        """
        Получает статистику операций по счету и возвращает как Pydantic-модель.

        :param account_id: ID счета для фильтрации операций.
        :return: Pydantic-модель со статистикой операций.
        """
        query = GetOperationsSummaryQuerySchema(account_id=account_id)
        response = self.get_operations_summary_api(query)
        return GetOperationsSummaryResponseSchema.model_validate_json(response.text)

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseSchema:
        """
        Создает операцию комиссии.
        Все данные (status, amount) генерируются автоматически.

        :param card_id: ID карты для операции.
        :param account_id: ID счета для операции.
        :return: Pydantic-модель с данными созданной операции.
        """
        # Теперь передаем только card_id и account_id, остальное генерируется автоматически
        request = MakeFeeOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_fee_operation_api(request)
        return MakeFeeOperationResponseSchema.model_validate_json(response.text)

    def make_top_up_operation(self, card_id: str, account_id: str) -> MakeTopUpOperationResponseSchema:
        """
        Создает операцию пополнения счета.
        Все данные (status, amount) генерируются автоматически.

        :param card_id: ID карты для операции.
        :param account_id: ID счета для операции.
        :return: Pydantic-модель с данными созданной операции.
        """
        # Теперь передаем только card_id и account_id, остальное генерируется автоматически
        request = MakeTopUpOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_top_up_operation_api(request)
        return MakeTopUpOperationResponseSchema.model_validate_json(response.text)

    def make_cashback_operation(self, card_id: str, account_id: str) -> MakeCashbackOperationResponseSchema:
        """
        Создает операцию начисления кэшбэка.
        Все данные (status, amount) генерируются автоматически.

        :param card_id: ID карты для операции.
        :param account_id: ID счета для операции.
        :return: Pydantic-модель с данными созданной операции.
        """
        # Теперь передаем только card_id и account_id, остальное генерируется автоматически
        request = MakeCashbackOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_cashback_operation_api(request)
        return MakeCashbackOperationResponseSchema.model_validate_json(response.text)

    def make_transfer_operation(self, card_id: str, account_id: str) -> MakeTransferOperationResponseSchema:
        """
        Создает операцию перевода средств.
        Все данные (status, amount) генерируются автоматически.

        :param card_id: ID карты для операции.
        :param account_id: ID счета для операции.
        :return: Pydantic-модель с данными созданной операции.
        """
        # Теперь передаем только card_id и account_id, остальное генерируется автоматически
        request = MakeTransferOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_transfer_operation_api(request)
        return MakeTransferOperationResponseSchema.model_validate_json(response.text)

    def make_purchase_operation(self, card_id: str, account_id: str) -> MakePurchaseOperationResponseSchema:
        """
        Создает операцию покупки.
        Все данные (status, amount, category) генерируются автоматически.

        :param card_id: ID карты для операции.
        :param account_id: ID счета для операции.
        :return: Pydantic-модель с данными созданной операции.
        """
        # Теперь передаем только card_id и account_id, остальное генерируется автоматически
        request = MakePurchaseOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_purchase_operation_api(request)
        return MakePurchaseOperationResponseSchema.model_validate_json(response.text)

    def make_bill_payment_operation(self, card_id: str, account_id: str) -> MakeBillPaymentOperationResponseSchema:
        """
        Создает операцию оплаты счета.
        Все данные (status, amount) генерируются автоматически.

        :param card_id: ID карты для операции.
        :param account_id: ID счета для операции.
        :return: Pydantic-модель с данными созданной операции.
        """
        # Теперь передаем только card_id и account_id, остальное генерируется автоматически
        request = MakeBillPaymentOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_bill_payment_operation_api(request)
        return MakeBillPaymentOperationResponseSchema.model_validate_json(response.text)

    def make_cash_withdrawal_operation(self, card_id: str,
                                       account_id: str) -> MakeCashWithdrawalOperationResponseSchema:
        """
        Создает операцию снятия наличных средств.
        Все данные (status, amount) генерируются автоматически.

        :param card_id: ID карты для операции.
        :param account_id: ID счета для операции.
        :return: Pydantic-модель с данными созданной операции.
        """
        # Теперь передаем только card_id и account_id, остальное генерируется автоматически
        request = MakeCashWithdrawalOperationRequestSchema(
            card_id=card_id,
            account_id=account_id
        )
        response = self.make_cash_withdrawal_operation_api(request)
        return MakeCashWithdrawalOperationResponseSchema.model_validate_json(response.text)


def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """
    Функция создаёт экземпляр OperationsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию OperationsGatewayHTTPClient.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())
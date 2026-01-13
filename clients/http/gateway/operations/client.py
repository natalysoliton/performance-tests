"""API клиент для работы с эндпоинтами операций сервиса http-gateway."""

from typing import TypedDict, Optional, Dict, Any, Union
import httpx
from ...client import HTTPClient


# ===================== Базовые типы запросов =====================

class BaseOperationQuery(TypedDict):
    """Базовый тип для параметров запросов операций."""
    accountId: str


class BaseOperationRequest(TypedDict):
    """Базовый тип для создания операций."""
    status: str
    amount: float
    cardId: str
    accountId: str


# ===================== Типы для GET запросов =====================

class GetOperationQuery(TypedDict):
    """Параметры для получения информации об операции."""
    operation_id: str


class GetOperationReceiptQuery(TypedDict):
    """Параметры для получения чека операции."""
    operation_id: str


class GetOperationsQuery(BaseOperationQuery):
    """Параметры для получения списка операций."""
    limit: Optional[int]
    offset: Optional[int]
    startDate: Optional[str]
    endDate: Optional[str]
    operationType: Optional[str]


class GetOperationsSummaryQuery(BaseOperationQuery):
    """Параметры для получения статистики по операциям."""
    startDate: Optional[str]
    endDate: Optional[str]
    groupBy: Optional[str]  # Например: "day", "week", "month", "category"


# ===================== Типы для POST запросов =====================

class MakeFeeOperationRequest(BaseOperationRequest):
    """Данные для создания операции комиссии."""
    feeType: str
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]


class MakeTopUpOperationRequest(BaseOperationRequest):
    """Данные для создания операции пополнения."""
    source: str  # Например: "bank_transfer", "card", "cash"
    currency: str
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]


class MakeCashbackOperationRequest(BaseOperationRequest):
    """Данные для создания операции кэшбэка."""
    cashbackType: str  # Например: "standard", "bonus", "promo"
    merchantId: Optional[str]
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]


class MakeTransferOperationRequest(BaseOperationRequest):
    """Данные для создания операции перевода."""
    recipientAccountId: str
    recipientName: str
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]


class MakePurchaseOperationRequest(BaseOperationRequest):
    """Данные для создания операции покупки."""
    merchantId: str
    merchantName: str
    category: str
    location: Optional[str]
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]


class MakeBillPaymentOperationRequest(BaseOperationRequest):
    """Данные для создания операции оплаты по счету."""
    billNumber: str
    billType: str  # Например: "utilities", "tax", "internet"
    providerName: str
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]


class MakeCashWithdrawalOperationRequest(BaseOperationRequest):
    """Данные для создания операции снятия наличных."""
    atmId: Optional[str]
    atmLocation: Optional[str]
    currency: str
    description: Optional[str]
    metadata: Optional[Dict[str, Any]]


class OperationsGatewayHTTPClient(HTTPClient):
    """Клиент для работы с API операций сервиса http-gateway."""
    
    def __init__(self, base_url: str, timeout: float = 10.0):
        """
        Инициализация клиента для работы с API операций.
        
        Args:
            base_url: Базовый URL сервиса http-gateway
            timeout: Таймаут запросов в секундах
        """
        super().__init__(base_url, timeout)
    
    # ===================== GET методы =====================
    
    def get_operation_api(self, operation_id: str) -> httpx.Response:
        """
        Получение информации об операции по её идентификатору.
        
        Выполняет GET-запрос к эндпоинту /api/v1/operations/{operation_id}
        
        Args:
            operation_id: Уникальный идентификатор операции
            
        Returns:
            httpx.Response: Объект ответа от сервера с информацией об операции
        """
        endpoint = f"/api/v1/operations/{operation_id}"
        
        with self._get_client() as client:
            response = client.get(
                url=endpoint,
                headers={"Accept": "application/json"}
            )
            return response
    
    def get_operation_receipt_api(self, operation_id: str) -> httpx.Response:
        """
        Получение чека по операции по её идентификатору.
        
        Выполняет GET-запрос к эндпоинту 
        /api/v1/operations/operation-receipt/{operation_id}
        
        Args:
            operation_id: Уникальный идентификатор операции
            
        Returns:
            httpx.Response: Объект ответа от сервера с чеком операции
        """
        endpoint = f"/api/v1/operations/operation-receipt/{operation_id}"
        
        with self._get_client() as client:
            response = client.get(
                url=endpoint,
                headers={"Accept": "application/json"}
            )
            return response
    
    def get_operations_api(self, query_params: GetOperationsQuery) -> httpx.Response:
        """
        Получение списка операций для определённого счёта.
        
        Выполняет GET-запрос к эндпоинту /api/v1/operations
        с параметрами фильтрации.
        
        Args:
            query_params: Параметры запроса, содержащие:
                - accountId: Идентификатор счёта (обязательный)
                - limit: Ограничение количества операций (опционально)
                - offset: Смещение для пагинации (опционально)
                - startDate: Начальная дата периода (опционально)
                - endDate: Конечная дата периода (опционально)
                - operationType: Тип операции (опционально)
                
        Returns:
            httpx.Response: Объект ответа от сервера со списком операций
        """
        endpoint = "/api/v1/operations"
        
        with self._get_client() as client:
            response = client.get(
                url=endpoint,
                params=query_params,
                headers={"Accept": "application/json"}
            )
            return response
    
    def get_operations_summary_api(self, query_params: GetOperationsSummaryQuery) -> httpx.Response:
        """
        Получение статистики по операциям для определённого счёта.
        
        Выполняет GET-запрос к эндпоинту /api/v1/operations/operations-summary
        с параметрами группировки.
        
        Args:
            query_params: Параметры запроса, содержащие:
                - accountId: Идентификатор счёта (обязательный)
                - startDate: Начальная дата периода (опционально)
                - endDate: Конечная дата периода (опционально)
                - groupBy: Параметр группировки (опционально)
                
        Returns:
            httpx.Response: Объект ответа от сервера со статистикой операций
        """
        endpoint = "/api/v1/operations/operations-summary"
        
        with self._get_client() as client:
            response = client.get(
                url=endpoint,
                params=query_params,
                headers={"Accept": "application/json"}
            )
            return response
    
    # ===================== POST методы =====================
    
    def make_fee_operation_api(self, request: MakeFeeOperationRequest) -> httpx.Response:
        """
        Создание операции комиссии.
        
        Выполняет POST-запрос к эндпоинту /api/v1/operations/make-fee-operation
        
        Args:
            request: Данные для создания операции комиссии, содержащие:
                - status: Статус операции
                - amount: Сумма операции
                - cardId: Идентификатор карты
                - accountId: Идентификатор счёта
                - feeType: Тип комиссии
                - description: Описание операции (опционально)
                - metadata: Дополнительные метаданные (опционально)
                
        Returns:
            httpx.Response: Объект ответа от сервера с результатом создания
        """
        endpoint = "/api/v1/operations/make-fee-operation"
        
        with self._get_client() as client:
            response = client.post(
                url=endpoint,
                json=request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            return response
    
    def make_top_up_operation_api(self, request: MakeTopUpOperationRequest) -> httpx.Response:
        """
        Создание операции пополнения.
        
        Выполняет POST-запрос к эндпоинту /api/v1/operations/make-top-up-operation
        
        Args:
            request: Данные для создания операции пополнения, содержащие:
                - status: Статус операции
                - amount: Сумма операции
                - cardId: Идентификатор карты
                - accountId: Идентификатор счёта
                - source: Источник пополнения
                - currency: Валюта операции
                - description: Описание операции (опционально)
                - metadata: Дополнительные метаданные (опционально)
                
        Returns:
            httpx.Response: Объект ответа от сервера с результатом создания
        """
        endpoint = "/api/v1/operations/make-top-up-operation"
        
        with self._get_client() as client:
            response = client.post(
                url=endpoint,
                json=request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            return response
    
    def make_cashback_operation_api(self, request: MakeCashbackOperationRequest) -> httpx.Response:
        """
        Создание операции кэшбэка.
        
        Выполняет POST-запрос к эндпоинту /api/v1/operations/make-cashback-operation
        
        Args:
            request: Данные для создания операции кэшбэка, содержащие:
                - status: Статус операции
                - amount: Сумма операции
                - cardId: Идентификатор карты
                - accountId: Идентификатор счёта
                - cashbackType: Тип кэшбэка
                - merchantId: Идентификатор мерчанта (опционально)
                - description: Описание операции (опционально)
                - metadata: Дополнительные метаданные (опционально)
                
        Returns:
            httpx.Response: Объект ответа от сервера с результатом создания
        """
        endpoint = "/api/v1/operations/make-cashback-operation"
        
        with self._get_client() as client:
            response = client.post(
                url=endpoint,
                json=request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            return response
    
    def make_transfer_operation_api(self, request: MakeTransferOperationRequest) -> httpx.Response:
        """
        Создание операции перевода.
        
        Выполняет POST-запрос к эндпоинту /api/v1/operations/make-transfer-operation
        
        Args:
            request: Данные для создания операции перевода, содержащие:
                - status: Статус операции
                - amount: Сумма операции
                - cardId: Идентификатор карты
                - accountId: Идентификатор счёта
                - recipientAccountId: Идентификатор счёта получателя
                - recipientName: Имя получателя
                - description: Описание операции (опционально)
                - metadata: Дополнительные метаданные (опционально)
                
        Returns:
            httpx.Response: Объект ответа от сервера с результатом создания
        """
        endpoint = "/api/v1/operations/make-transfer-operation"
        
        with self._get_client() as client:
            response = client.post(
                url=endpoint,
                json=request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            return response
    
    def make_purchase_operation_api(self, request: MakePurchaseOperationRequest) -> httpx.Response:
        """
        Создание операции покупки.
        
        Выполняет POST-запрос к эндпоинту /api/v1/operations/make-purchase-operation
        
        Args:
            request: Данные для создания операции покупки, содержащие:
                - status: Статус операции
                - amount: Сумма операции
                - cardId: Идентификатор карты
                - accountId: Идентификатор счёта
                - merchantId: Идентификатор мерчанта
                - merchantName: Название мерчанта
                - category: Категория покупки
                - location: Местоположение (опционально)
                - description: Описание операции (опционально)
                - metadata: Дополнительные метаданные (опционально)
                
        Returns:
            httpx.Response: Объект ответа от сервера с результатом создания
        """
        endpoint = "/api/v1/operations/make-purchase-operation"
        
        with self._get_client() as client:
            response = client.post(
                url=endpoint,
                json=request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            return response
    
    def make_bill_payment_operation_api(self, request: MakeBillPaymentOperationRequest) -> httpx.Response:
        """
        Создание операции оплаты по счету.
        
        Выполняет POST-запрос к эндпоинту /api/v1/operations/make-bill-payment-operation
        
        Args:
            request: Данные для создания операции оплаты по счету, содержащие:
                - status: Статус операции
                - amount: Сумма операции
                - cardId: Идентификатор карты
                - accountId: Идентификатор счёта
                - billNumber: Номер счёта
                - billType: Тип счёта
                - providerName: Название провайдера
                - description: Описание операции (опционально)
                - metadata: Дополнительные метаданные (опционально)
                
        Returns:
            httpx.Response: Объект ответа от сервера с результатом создания
        """
        endpoint = "/api/v1/operations/make-bill-payment-operation"
        
        with self._get_client() as client:
            response = client.post(
                url=endpoint,
                json=request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            return response
    
    def make_cash_withdrawal_operation_api(self, request: MakeCashWithdrawalOperationRequest) -> httpx.Response:
        """
        Создание операции снятия наличных денег.
        
        Выполняет POST-запрос к эндпоинту /api/v1/operations/make-cash-withdrawal-operation
        
        Args:
            request: Данные для создания операции снятия наличных, содержащие:
                - status: Статус операции
                - amount: Сумма операции
                - cardId: Идентификатор карты
                - accountId: Идентификатор счёта
                - atmId: Идентификатор банкомата (опционально)
                - atmLocation: Местоположение банкомата (опционально)
                - currency: Валюта операции
                - description: Описание операции (опционально)
                - metadata: Дополнительные метаданные (опционально)
                
        Returns:
            httpx.Response: Объект ответа от сервера с результатом создания
        """
        endpoint = "/api/v1/operations/make-cash-withdrawal-operation"
        
        with self._get_client() as client:
            response = client.post(
                url=endpoint,
                json=request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            return response

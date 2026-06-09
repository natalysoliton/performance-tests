"""
Pydantic-модели для клиента OperationsGatewayHTTPClient.

Этот модуль содержит все схемы данных для работы с операциями:
- OperationType: перечисление типов операций
- OperationStatus: перечисление статусов операций
- OperationSchema: базовая модель операции
- OperationReceiptSchema: модель чека операции
- OperationsSummarySchema: модель статистики операций
- GetOperationResponseSchema: ответ на получение операции
- GetOperationsQuerySchema: запрос на получение списка операций
- GetOperationsResponseSchema: ответ со списком операций
- GetOperationsSummaryQuerySchema: запрос на получение статистики
- GetOperationsSummaryResponseSchema: ответ со статистикой
- GetOperationReceiptResponseSchema: ответ с чеком операции
- MakeOperationRequestSchema: базовая модель запроса операции
- MakeFeeOperationRequestSchema: запрос на операцию комиссии
- MakeFeeOperationResponseSchema: ответ на операцию комиссии
- MakeTopUpOperationRequestSchema: запрос на операцию пополнения
- MakeTopUpOperationResponseSchema: ответ на операцию пополнения
- MakeCashbackOperationRequestSchema: запрос на операцию кэшбэка
- MakeCashbackOperationResponseSchema: ответ на операцию кэшбэка
- MakeTransferOperationRequestSchema: запрос на операцию перевода
- MakeTransferOperationResponseSchema: ответ на операцию перевода
- MakePurchaseOperationRequestSchema: запрос на операцию покупки
- MakePurchaseOperationResponseSchema: ответ на операцию покупки
- MakeBillPaymentOperationRequestSchema: запрос на оплату счета
- MakeBillPaymentOperationResponseSchema: ответ на оплату счета
- MakeCashWithdrawalOperationRequestSchema: запрос на снятие наличных
- MakeCashWithdrawalOperationResponseSchema: ответ на снятие наличных
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, ConfigDict, HttpUrl

# Импортируем заранее созданный экземпляр класса Fake
from tools.fakers import fake


class OperationType(StrEnum):
    """
    Тип операции.
    Возможные значения из Swagger-документации API.
    """
    FEE = "FEE"  # Комиссия
    TOP_UP = "TOP_UP"  # Пополнение
    CASHBACK = "CASHBACK"  # Кэшбэк
    TRANSFER = "TRANSFER"  # Перевод
    PURCHASE = "PURCHASE"  # Покупка
    BILL_PAYMENT = "BILL_PAYMENT"  # Оплата счета
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"  # Снятие наличных


class OperationStatus(StrEnum):
    """
    Статус операции.
    Возможные значения из Swagger-документации API.
    """
    PENDING = "PENDING"  # В обработке
    COMPLETED = "COMPLETED"  # Завершена
    FAILED = "FAILED"  # Ошибка
    CANCELLED = "CANCELLED"  # Отменена


class OperationSchema(BaseModel):
    """
    Описание структуры операции.

    Attributes:
        id: Уникальный идентификатор операции
        type: Тип операции
        status: Статус операции
        amount: Сумма операции
        card_id: ID карты, по которой выполнена операция
        category: Категория операции (для покупок)
        created_at: Дата и время создания операции
        account_id: ID счета, по которому выполнена операция
    """
    id: str
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: str = Field(alias="cardId")
    category: str | None = None
    created_at: datetime = Field(alias="createdAt")
    account_id: str = Field(alias="accountId")


class OperationReceiptSchema(BaseModel):
    """
    Описание структуры чека по операции.

    Attributes:
        url: URL-адрес чека
        document: Идентификатор или содержимое документа
    """
    url: HttpUrl
    document: str


class OperationsSummarySchema(BaseModel):
    """
    Описание структуры статистики по операциям.

    Attributes:
        spent_amount: Сумма потраченных средств
        received_amount: Сумма полученных средств
        cashback_amount: Сумма начисленного кэшбэка
    """
    spent_amount: float = Field(alias="spentAmount")
    received_amount: float = Field(alias="receivedAmount")
    cashback_amount: float = Field(alias="cashbackAmount")


class GetOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа получения операции.

    Attributes:
        operation: Объект операции
    """
    operation: OperationSchema


class GetOperationsQuerySchema(BaseModel):
    """
    Структура query параметров запроса для получения списка операций по счёту.

    Attributes:
        account_id: ID счета для фильтрации операций
    """
    model_config = ConfigDict(populate_by_name=True)

    account_id: str = Field(alias="accountId")


class GetOperationsResponseSchema(BaseModel):
    """
    Описание структуры ответа получения списка операций.

    Attributes:
        operations: Список операций
    """
    operations: list[OperationSchema]


class GetOperationsSummaryQuerySchema(BaseModel):
    """
    Структура query параметров запроса для получения статистики по операциям счёта.

    Attributes:
        account_id: ID счета для фильтрации операций
    """
    model_config = ConfigDict(populate_by_name=True)

    account_id: str = Field(alias="accountId")


class GetOperationsSummaryResponseSchema(BaseModel):
    """
    Описание структуры ответа получения статистики по операциям.

    Attributes:
        summary: Статистика по операциям
    """
    summary: OperationsSummarySchema


class GetOperationReceiptResponseSchema(BaseModel):
    """
    Описание структуры ответа получения чека по операции.

    Attributes:
        receipt: Чек операции
    """
    receipt: OperationReceiptSchema


class MakeOperationRequestSchema(BaseModel):
    """
    Базовая структура тела запроса для создания финансовой операции.

    Attributes:
        status: Статус операции (обычно COMPLETED)
        amount: Сумма операции
        card_id: ID карты для операции
        account_id: ID счета для операции
    """
    model_config = ConfigDict(populate_by_name=True)

    # Генерируем случайный статус операции из enum
    status: OperationStatus = Field(
        default_factory=lambda: fake.enum(OperationStatus)
    )
    # Генерируем случайную сумму операции
    amount: float = Field(default_factory=fake.amount)
    card_id: str = Field(alias="cardId")
    account_id: str = Field(alias="accountId")


class MakeFeeOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции комиссии.

    Наследует все поля от MakeOperationRequestSchema:
    - status (генерируется автоматически)
    - amount (генерируется автоматически)
    - card_id (обязательный параметр)
    - account_id (обязательный параметр)
    """
    pass


class MakeFeeOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции комиссии.

    Attributes:
        operation: Объект созданной операции
    """
    operation: OperationSchema


class MakeTopUpOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции пополнения.

    Наследует все поля от MakeOperationRequestSchema:
    - status (генерируется автоматически)
    - amount (генерируется автоматически)
    - card_id (обязательный параметр)
    - account_id (обязательный параметр)
    """
    pass


class MakeTopUpOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции пополнения.

    Attributes:
        operation: Объект созданной операции
    """
    operation: OperationSchema


class MakeCashbackOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции кэшбэка.

    Наследует все поля от MakeOperationRequestSchema:
    - status (генерируется автоматически)
    - amount (генерируется автоматически)
    - card_id (обязательный параметр)
    - account_id (обязательный параметр)
    """
    pass


class MakeCashbackOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции кэшбэка.

    Attributes:
        operation: Объект созданной операции
    """
    operation: OperationSchema


class MakeTransferOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции перевода.

    Наследует все поля от MakeOperationRequestSchema:
    - status (генерируется автоматически)
    - amount (генерируется автоматически)
    - card_id (обязательный параметр)
    - account_id (обязательный параметр)
    """
    pass


class MakeTransferOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции перевода.

    Attributes:
        operation: Объект созданной операции
    """
    operation: OperationSchema


class MakePurchaseOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции покупки.

    Attributes:
        category: Категория покупки (генерируется автоматически)

    Наследует от MakeOperationRequestSchema:
    - status (генерируется автоматически)
    - amount (генерируется автоматически)
    - card_id (обязательный параметр)
    - account_id (обязательный параметр)
    """
    # Генерируем случайную категорию покупки
    category: str = Field(default_factory=fake.category)


class MakePurchaseOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции покупки.

    Attributes:
        operation: Объект созданной операции
    """
    operation: OperationSchema


class MakeBillPaymentOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции оплаты по счёту.

    Наследует все поля от MakeOperationRequestSchema:
    - status (генерируется автоматически)
    - amount (генерируется автоматически)
    - card_id (обязательный параметр)
    - account_id (обязательный параметр)
    """
    pass


class MakeBillPaymentOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции оплаты по счёту.

    Attributes:
        operation: Объект созданной операции
    """
    operation: OperationSchema


class MakeCashWithdrawalOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции снятия наличных.

    Наследует все поля от MakeOperationRequestSchema:
    - status (генерируется автоматически)
    - amount (генерируется автоматически)
    - card_id (обязательный параметр)
    - account_id (обязательный параметр)
    """
    pass


class MakeCashWithdrawalOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции снятия наличных.

    Attributes:
        operation: Объект созданной операции
    """
    operation: OperationSchema
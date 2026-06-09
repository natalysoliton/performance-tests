from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, ConfigDict, HttpUrl


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
    category: str | None = None  # Категория может отсутствовать для некоторых типов операций
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

    status: OperationStatus
    amount: float
    card_id: str = Field(alias="cardId")
    account_id: str = Field(alias="accountId")


class MakeFeeOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции комиссии.
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
        category: Категория покупки
    """
    category: str


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
    """
    pass


class MakeCashWithdrawalOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции снятия наличных.

    Attributes:
        operation: Объект созданной операции
    """
    operation: OperationSchema
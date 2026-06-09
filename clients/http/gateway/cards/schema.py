"""
Pydantic-модели для клиента CardsGatewayHTTPClient.

Этот модуль содержит все схемы данных для работы с картами:
- CardSchema: базовая модель карты
- Enum-классы для ограниченных значений (тип, статус, платежная система)
- IssueVirtualCardRequestSchema: запрос на выпуск виртуальной карты
- IssueVirtualCardResponseSchema: ответ на выпуск виртуальной карты
- IssuePhysicalCardRequestSchema: запрос на выпуск физической карты
- IssuePhysicalCardResponseSchema: ответ на выпуск физической карты
"""

from datetime import date
from enum import StrEnum

from pydantic import BaseModel, Field, ConfigDict


class CardType(StrEnum):
    """
    Тип карты.
    Возможные значения из Swagger-документации API.
    """
    VIRTUAL = "VIRTUAL"
    PHYSICAL = "PHYSICAL"


class CardStatus(StrEnum):
    """
    Статус карты.
    Возможные значения из Swagger-документации API.
    """
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"


class CardPaymentSystem(StrEnum):
    """
    Платежная система карты.
    Возможные значения из Swagger-документации API.
    """
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"


class CardSchema(BaseModel):
    """
    Описание структуры карты.

    Attributes:
        id: Уникальный идентификатор карты
        pin: PIN-код карты
        cvv: CVV-код карты
        type: Тип карты (VIRTUAL/PHYSICAL)
        status: Статус карты (ACTIVE/FROZEN/CLOSED/BLOCKED)
        account_id: ID счета, к которому привязана карта
        card_number: Номер карты
        card_holder: Имя держателя карты
        expiry_date: Дата истечения срока действия карты
        payment_system: Платежная система (VISA/MASTERCARD)
    """
    id: str
    pin: str
    cvv: str
    type: CardType
    status: CardStatus
    account_id: str = Field(alias="accountId")
    card_number: str = Field(alias="cardNumber")
    card_holder: str = Field(alias="cardHolder")
    expiry_date: date = Field(alias="expiryDate")
    payment_system: CardPaymentSystem = Field(alias="paymentSystem")


class IssueVirtualCardRequestSchema(BaseModel):
    """
    Структура данных для выпуска виртуальной карты.

    Attributes:
        user_id: ID пользователя, которому выпускается карта
        account_id: ID счета, к которому привязывается карта
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")
    account_id: str = Field(alias="accountId")


class IssueVirtualCardResponseSchema(BaseModel):
    """
    Описание структуры ответа выпуска виртуальной карты.

    Attributes:
        card: Объект карты (CardSchema)
    """
    card: CardSchema


class IssuePhysicalCardRequestSchema(BaseModel):
    """
    Структура данных для выпуска физической карты.

    Attributes:
        user_id: ID пользователя, которому выпускается карта
        account_id: ID счета, к которому привязывается карта
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")
    account_id: str = Field(alias="accountId")


class IssuePhysicalCardResponseSchema(BaseModel):
    """
    Описание структуры ответа выпуска физической карты.

    Attributes:
        card: Объект карты (CardSchema)
    """
    card: CardSchema
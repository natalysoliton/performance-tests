from enum import StrEnum

from pydantic import BaseModel, Field, ConfigDict

from clients.http.gateway.cards.schema import CardSchema


class AccountType(StrEnum):
    """
    Тип счета.
    Возможные значения из Swagger-документации API.
    """
    DEPOSIT = "DEPOSIT"  # Депозитный счет
    SAVINGS = "SAVINGS"  # Сберегательный счет
    DEBIT_CARD = "DEBIT_CARD"  # Дебетовый счет
    CREDIT_CARD = "CREDIT_CARD"  # Кредитный счет


class AccountStatus(StrEnum):
    """
    Статус счета.
    Возможные значения из Swagger-документации API.
    """
    ACTIVE = "ACTIVE"  # Активный
    CLOSED = "CLOSED"  # Закрытый
    PENDING_CLOSURE = "PENDING_CLOSURE"  # Ожидает закрытия


class AccountSchema(BaseModel):
    """
    Описание структуры аккаунта.

    Attributes:
        id: Уникальный идентификатор счета
        type: Тип счета (DEPOSIT/SAVINGS/DEBIT_CARD/CREDIT_CARD)
        cards: Список карт, привязанных к счету
        status: Статус счета (ACTIVE/CLOSED/PENDING_CLOSURE)
        balance: Текущий баланс счета
    """
    id: str
    type: AccountType
    cards: list[CardSchema]
    status: AccountStatus
    balance: float


class GetAccountsQuerySchema(BaseModel):
    """
    Структура данных для получения списка счетов пользователя.

    Attributes:
        user_id: ID пользователя, чьи счета нужно получить
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")


class GetAccountsResponseSchema(BaseModel):
    """
    Описание структуры ответа получения списка счетов.

    Attributes:
        accounts: Список счетов пользователя
    """
    accounts: list[AccountSchema]


class OpenDepositAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия депозитного счета.

    Attributes:
        user_id: ID пользователя, для которого открывается счет
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")


class OpenDepositAccountResponseSchema(BaseModel):
    """
    Описание структуры ответа открытия депозитного счета.

    Attributes:
        account: Информация об открытом депозитном счете
    """
    account: AccountSchema


class OpenSavingsAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия сберегательного счета.

    Attributes:
        user_id: ID пользователя, для которого открывается счет
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")


class OpenSavingsAccountResponseSchema(BaseModel):
    """
    Описание структуры ответа открытия сберегательного счета.

    Attributes:
        account: Информация об открытом сберегательном счете
    """
    account: AccountSchema


class OpenDebitCardAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия дебетового счета.

    Attributes:
        user_id: ID пользователя, для которого открывается счет
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")


class OpenDebitCardAccountResponseSchema(BaseModel):
    """
    Описание структуры ответа открытия дебетового счета.

    Attributes:
        account: Информация об открытом дебетовом счете
    """
    account: AccountSchema


class OpenCreditCardAccountRequestSchema(BaseModel):
    """
    Структура данных для открытия кредитного счета.

    Attributes:
        user_id: ID пользователя, для которого открывается счет
    """
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")


class OpenCreditCardAccountResponseSchema(BaseModel):
    """
    Описание структуры ответа открытия кредитного счета.

    Attributes:
        account: Информация об открытом кредитном счете
    """
    account: AccountSchema
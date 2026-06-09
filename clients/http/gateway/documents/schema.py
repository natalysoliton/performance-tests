from pydantic import BaseModel, HttpUrl


class DocumentSchema(BaseModel):
    """
    Описание структуры документа.

    Attributes:
        url: URL-адрес документа (валидируется как HttpUrl)
        document: Содержимое или идентификатор документа
    """
    url: HttpUrl  # Используем HttpUrl для автоматической валидации URL
    document: str


class GetTariffDocumentResponseSchema(BaseModel):
    """
    Описание структуры ответа получения документа тарифа.

    Attributes:
        tariff: Объект документа с тарифом
    """
    tariff: DocumentSchema


class GetContractDocumentResponseSchema(BaseModel):
    """
    Описание структуры ответа получения документа контракта.

    Attributes:
        contract: Объект документа с контрактом
    """
    contract: DocumentSchema
"""
HTTP-клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
Использует Pydantic-модели для валидации запросов и ответов.
"""

from httpx import Response

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.documents.schema import (
    GetTariffDocumentResponseSchema,
    GetContractDocumentResponseSchema
)


# Все TypedDict модели удалены, теперь используются Pydantic-модели из schema.py


class DocumentsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.

    Предоставляет методы для работы с документами:
    - Получение тарифного документа по ID счета
    - Получение контрактного документа по ID счета
    """

    def get_tariff_document_api(self, account_id: str) -> Response:
        """
        Получить тарифный документ по счету (низкоуровневый метод).

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/documents/tariff-document/{account_id}")

    def get_contract_document_api(self, account_id: str) -> Response:
        """
        Получить контрактный документ по счету (низкоуровневый метод).

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/documents/contract-document/{account_id}")

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseSchema:
        """
        Получить тарифный документ и вернуть как Pydantic-модель.

        :param account_id: Идентификатор счета.
        :return: Pydantic-модель с данными тарифного документа.
        """
        response = self.get_tariff_document_api(account_id)
        # Используем model_validate_json для безопасной десериализации
        return GetTariffDocumentResponseSchema.model_validate_json(response.text)

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseSchema:
        """
        Получить контрактный документ и вернуть как Pydantic-модель.

        :param account_id: Идентификатор счета.
        :return: Pydantic-модель с данными контрактного документа.
        """
        response = self.get_contract_document_api(account_id)
        # Используем model_validate_json для безопасной десериализации
        return GetContractDocumentResponseSchema.model_validate_json(response.text)


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """
    Функция создаёт экземпляр DocumentsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())
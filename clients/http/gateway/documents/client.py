from httpx import Response
from locust.env import Environment

from clients.http.client import HTTPClient, HTTPClientExtensions
from clients.http.gateway.client import (
    build_gateway_http_client,
    build_gateway_locust_http_client
)
from clients.http.gateway.documents.schema import (
    GetTariffDocumentResponseSchema,
    GetContractDocumentResponseSchema
)
from tools.routes import APIRoutes  # Импортируем enum APIRoutes


class DocumentsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/documents сервиса http-gateway.
    """

    def get_tariff_document_api(self, account_id: str) -> Response:
        """
        Получить тарифный документ по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(
            f"{APIRoutes.DOCUMENTS}/tariff-document/{account_id}",
            extensions=HTTPClientExtensions(route=f"{APIRoutes.DOCUMENTS}/tariff-document/{{account_id}}")
        )

    def get_contract_document_api(self, account_id: str) -> Response:
        """
        Получить контрактный документ по счету.

        :param account_id: Идентификатор счета.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(
            f"{APIRoutes.DOCUMENTS}/contract-document/{account_id}",
            extensions=HTTPClientExtensions(route=f"{APIRoutes.DOCUMENTS}/contract-document/{{account_id}}")
        )

    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseSchema:
        """
        Получить тарифный документ и вернуть как Pydantic-модель.

        :param account_id: Идентификатор счета.
        :return: Pydantic-модель с данными тарифного документа.
        """
        response = self.get_tariff_document_api(account_id)
        return GetTariffDocumentResponseSchema.model_validate_json(response.text)

    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseSchema:
        """
        Получить контрактный документ и вернуть как Pydantic-модель.

        :param account_id: Идентификатор счета.
        :return: Pydantic-модель с данными контрактного документа.
        """
        response = self.get_contract_document_api(account_id)
        return GetContractDocumentResponseSchema.model_validate_json(response.text)


def build_documents_gateway_http_client() -> DocumentsGatewayHTTPClient:
    """
    Функция создаёт экземпляр DocumentsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию DocumentsGatewayHTTPClient.
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_http_client())


def build_documents_gateway_locust_http_client(environment: Environment) -> DocumentsGatewayHTTPClient:
    """
    Создаёт экземпляр DocumentsGatewayHTTPClient, адаптированный для нагрузочного тестирования с Locust.

    В отличие от стандартного билдера, этот клиент:
    - использует HTTP-клиент со встроенными event_hooks для сбора метрик
    - автоматически передаёт метрики (время ответа, статус, размер) в Locust
    - отключает избыточное логирование HTTPX для чистоты вывода

    Билдер предназначен исключительно для использования внутри load-тестов Locust.
    Для обычных автотестов используйте build_documents_gateway_http_client().

    :param environment: Объект окружения Locust, необходим для отправки метрик через events.request
    :return: Экземпляр DocumentsGatewayHTTPClient с настроенным HTTP-клиентом для сбора метрик
    """
    return DocumentsGatewayHTTPClient(client=build_gateway_locust_http_client(environment))

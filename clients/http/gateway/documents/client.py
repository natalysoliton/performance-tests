"""API клиент для работы с эндпоинтами документов сервиса http-gateway."""

from typing import TypedDict, Optional
import httpx
from ...client import HTTPClient


class DocumentDict(TypedDict):
    """Типизированный словарь для описания документа."""
    url: str
    document: str


class GetTariffDocumentResponseDict(TypedDict):
    """Типизированный словарь для ответа с документом тарифа."""
    tariff: DocumentDict


class GetContractDocumentResponseDict(TypedDict):
    """Типизированный словарь для ответа с документом контракта."""
    contract: DocumentDict


class GetTariffDocumentQuery(TypedDict):
    """Параметры для получения документа тарифа."""
    account_id: str


class GetContractDocumentQuery(TypedDict):
    """Параметры для получения документа контракта."""
    account_id: str


class DocumentsGatewayHTTPClient(HTTPClient):
    """Клиент для работы с API документов сервиса http-gateway."""
    
    def __init__(self, base_url: str, timeout: float = 10.0):
        """
        Инициализация клиента для работы с API документов.
        
        Args:
            base_url: Базовый URL сервиса http-gateway
            timeout: Таймаут запросов в секундах
        """
        super().__init__(base_url, timeout)
    
    def get_tariff_document_api(self, account_id: str) -> httpx.Response:
        """
        Получение документа тарифа по идентификатору счёта.
        
        Выполняет GET-запрос к эндпоинту /api/v1/documents/tariff-document
        
        Args:
            account_id: Идентификатор счёта
            
        Returns:
            httpx.Response: Объект ответа от сервера с документом тарифа
        """
        endpoint = "/api/v1/documents/tariff-document"
        params = {"accountId": account_id}
        
        with self._get_client() as client:
            response = client.get(
                url=endpoint,
                params=params,
                headers={"Accept": "application/json"}
            )
            return response
    
    def get_contract_document_api(self, account_id: str) -> httpx.Response:
        """
        Получение документа контракта по идентификатору счёта.
        
        Выполняет GET-запрос к эндпоинту /api/v1/documents/contract-document
        
        Args:
            account_id: Идентификатор счёта
            
        Returns:
            httpx.Response: Объект ответа от сервера с документом контракта
        """
        endpoint = "/api/v1/documents/contract-document"
        params = {"accountId": account_id}
        
        with self._get_client() as client:
            response = client.get(
                url=endpoint,
                params=params,
                headers={"Accept": "application/json"}
            )
            return response
    
    def get_tariff_document(self, account_id: str) -> GetTariffDocumentResponseDict:
        """
        Высокоуровневый метод для получения документа тарифа.
        
        Извлекает JSON-ответ из API и возвращает его в типизированном виде.
        
        Args:
            account_id: Идентификатор счёта
            
        Returns:
            GetTariffDocumentResponseDict: Словарь с документом тарифа
            
        Raises:
            httpx.HTTPStatusError: Если запрос завершился с ошибкой
        """
        response = self.get_tariff_document_api(account_id)
        response.raise_for_status()  # Проверяем успешность запроса
        return response.json()
    
    def get_contract_document(self, account_id: str) -> GetContractDocumentResponseDict:
        """
        Высокоуровневый метод для получения документа контракта.
        
        Извлекает JSON-ответ из API и возвращает его в типизированном виде.
        
        Args:
            account_id: Идентификатор счёта
            
        Returns:
            GetContractDocumentResponseDict: Словарь с документом контракта
            
        Raises:
            httpx.HTTPStatusError: Если запрос завершился с ошибкой
        """
        response = self.get_contract_document_api(account_id)
        response.raise_for_status()  # Проверяем успешность запроса
        return response.json()

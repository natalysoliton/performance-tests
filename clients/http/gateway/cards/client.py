"""API клиент для работы с эндпоинтами карт сервиса http-gateway."""

from typing import TypedDict, Optional, Dict, Any
import httpx
from ...client import HTTPClient


class VirtualCardRequest(TypedDict):
    """Типизированный словарь для запроса создания виртуальной карты."""
    user_id: str
    account_id: str
    currency: str
    card_type: Optional[str]
    metadata: Optional[Dict[str, Any]]


class PhysicalCardRequest(TypedDict):
    """Типизированный словарь для запроса создания физической карты."""
    user_id: str
    account_id: str
    currency: str
    delivery_address: str
    card_holder_name: str
    card_type: Optional[str]
    metadata: Optional[Dict[str, Any]]


class CardsGatewayHTTPClient(HTTPClient):
    """Клиент для работы с API карт сервиса http-gateway."""

    def __init__(self, base_url: str, timeout: float = 10.0):
        """
        Инициализация клиента для работы с API карт.

        Args:
            base_url: Базовый URL сервиса http-gateway
            timeout: Таймаут запросов в секундах
        """
        super().__init__(base_url, timeout)

    def issue_virtual_card_api(self, request: VirtualCardRequest) -> httpx.Response:
        """
        Создание виртуальной карты через API.

        Выполняет POST-запрос к эндпоинту /api/v1/cards/issue-virtual-card
        для создания виртуальной карты.

        Args:
            request: Словарь с данными для создания виртуальной карты.
                    Должен содержать обязательные поля:
                    - user_id: Идентификатор пользователя
                    - account_id: Идентификатор счета
                    - currency: Валюта карты (например, "RUB", "USD")
                    Опциональные поля:
                    - card_type: Тип карты (например, "debit", "credit")
                    - metadata: Дополнительные метаданные в виде словаря

        Returns:
            httpx.Response: Объект ответа от сервера, содержащий статус код,
                           заголовки и тело ответа.

        Examples:
            >>> client = CardsGatewayHTTPClient("http://localhost:8080")
            >>> request_data = {
            ...     "user_id": "user123",
            ...     "account_id": "acc456",
            ...     "currency": "RUB",
            ...     "card_type": "debit"
            ... }
            >>> response = client.issue_virtual_card_api(request_data)
            >>> print(response.status_code)
            201
        """
        endpoint = "/api/v1/cards/issue-virtual-card"

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

    def issue_physical_card_api(self, request: PhysicalCardRequest) -> httpx.Response:
        """
        Создание физической карты через API.

        Выполняет POST-запрос к эндпоинту /api/v1/cards/issue-physical-card
        для создания физической карты с доставкой.

        Args:
            request: Словарь с данными для создания физической карты.
                    Должен содержать обязательные поля:
                    - user_id: Идентификатор пользователя
                    - account_id: Идентификатор счета
                    - currency: Валюта карты (например, "RUB", "USD")
                    - delivery_address: Адрес доставки карты
                    - card_holder_name: Имя держателя карты
                    Опциональные поля:
                    - card_type: Тип карты (например, "debit", "credit")
                    - metadata: Дополнительные метаданные в виде словаря

        Returns:
            httpx.Response: Объект ответа от сервера, содержащий статус код,
                           заголовки и тело ответа.

        Examples:
            >>> client = CardsGatewayHTTPClient("http://localhost:8080")
            >>> request_data = {
            ...     "user_id": "user123",
            ...     "account_id": "acc456",
            ...     "currency": "RUB",
            ...     "delivery_address": "г. Москва, ул. Примерная, д. 1",
            ...     "card_holder_name": "Иванов Иван Иванович",
            ...     "card_type": "credit"
            ... }
            >>> response = client.issue_physical_card_api(request_data)
            >>> print(response.status_code)
            201
        """
        endpoint = "/api/v1/cards/issue-physical-card"

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

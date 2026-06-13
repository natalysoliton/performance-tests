import logging

from locust.env import Environment  # Импорт окружения Locust для передачи в хуки

from clients.http.event_hooks.locust_event_hook import (
    locust_request_event_hook,  # Хук для отслеживания начала запроса
    locust_response_event_hook  # Хук для сбора метрик по завершении запроса
)
from typing import Any, TypedDict

from httpx import Client, Response, QueryParams, URL


# Тип расширений, которые можно передать в запрос
# В нашем случае мы используем только параметр "route", но можно добавить и другие
class HTTPClientExtensions(TypedDict, total=False):
    route: str


class HTTPClient:
    """
    Базовый HTTP API клиент, принимающий объект httpx.Client.

    :param client: экземпляр httpx.Client для выполнения HTTP-запросов
    """

    def __init__(self, client: Client) -> None:
        self.client = client

    def get(
            self,
            url: str | URL,
            params: QueryParams | None = None,
            extensions: HTTPClientExtensions | None = None  # Добавили поддержку extensions
    ) -> Response:
        """
        Выполняет GET-запрос.

        :param url: URL-адрес эндпоинта.
        :param params: GET-параметры запроса (например, ?key=value).
        :param extensions: Дополнительные данные, передаваемые через HTTPX extensions.
        :return: Объект Response с данными ответа.
        """
        return self.client.get(url=url, params=params, extensions=extensions)  # Передаём extensions в httpx.Client

    def post(
            self,
            url: str | URL,
            json: Any | None = None,
            extensions: HTTPClientExtensions | None = None  # Поддержка extensions для POST-запросов
    ) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL-адрес эндпоинта.
        :param json: Данные в формате JSON.
        :param extensions: Дополнительные данные, передаваемые через HTTPX extensions.
        :return: Объект Response с данными ответа.
        """
        return self.client.post(url=url, json=json, extensions=extensions)  # extensions передаётся в httpx.Client


def build_gateway_http_client() -> Client:
    """
    Функция создаёт экземпляр httpx.Client с базовыми настройками для сервиса http-gateway.

    :return: Готовый к использованию объект httpx.Client.
    """
    return Client(timeout=100, base_url="http://localhost:8003")


def build_gateway_locust_http_client(environment: Environment) -> Client:
    """
    HTTP-клиент, предназначенный специально для нагрузочного тестирования с помощью Locust.

    Отличается от обычного клиента тем, что:
    - добавляет хук `locust_request_event_hook` для фиксации времени начала запроса,
    - добавляет хук `locust_response_event_hook`, который вычисляет метрики
    (время ответа, длину ответа и т.д.) и отправляет их в Locust через `environment.events.request`.

    Таким образом, данный клиент автоматически репортит статистику в Locust
    при каждом выполненном HTTP-запросе.

    :param environment: Объект окружения Locust, необходим для генерации событий метрик.
    :return: httpx.Client с подключёнными хуками под нагрузочное тестирование.
    """
    # Подавляем INFO-логи httpx (например: "HTTP Request: GET ... 200 OK")
    # Это избавляет консоль от лишнего вывода при высоконагруженных тестах
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return Client(
        timeout=100,
        base_url="http://localhost:8003",
        event_hooks={
            "request": [locust_request_event_hook],  # Отмечаем время начала запроса
            "response": [locust_response_event_hook(environment)]  # Собираем метрики и передаём их в Locust
        }
    )

from httpx import Client
from locust.env import Environment
import logging
from clients.http.event_hooks.locust_event_hook import (
    locust_request_event_hook,
    locust_response_event_hook
)

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
    - добавляет хук 'locust_request_event_hook' для фиксации времени начала запроса.
    - добавляет хук 'locust_response_event_hook', который вычисляет метрики
    (время ответа, длину(величину) ответа и т.д.) и отправляет их в Locust через 'environment.events.request'.

    таким образом, данный клиент автоматически репортит статистику в Locust
    при каждом выполненном HTTP-запросе.

    :param environment: Объект окружения Locust, необходим для генерации событий метрик.
    :return: httpx.Client с подключенными хуками под нагрузочное тестирование.
    """
    logging.getLogger("httpx").setLevel(logging.WARNING)
    return Client(
        timeout=100,
        base_url="http://localhost:8003",
        event_hooks={
            "request": [locust_request_event_hook],
            "response": [locust_response_event_hook(environment)]
        }
    )

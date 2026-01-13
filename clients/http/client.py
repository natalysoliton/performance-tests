"""Базовый HTTP клиент для работы с API."""

import httpx


class HTTPClient:
    """Базовый класс HTTP клиента для выполнения запросов."""

    def __init__(self, base_url: str, timeout: float = 10.0):
        """
        Инициализация HTTP клиента.

        Args:
            base_url: Базовый URL API сервера
            timeout: Таймаут запросов в секундах
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout

    def _get_client(self) -> httpx.Client:
        """Создает и возвращает HTTP клиент."""
        return httpx.Client(base_url=self.base_url, timeout=self.timeout)

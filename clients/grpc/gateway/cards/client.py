"""
gRPC API клиент для взаимодействия с CardsGatewayService.

Предоставляет методы для работы с банковскими картами:
- Выпуск виртуальной карты (IssueVirtualCard)
- Выпуск физической карты (IssuePhysicalCard)

Структура методов:
- Низкоуровневые API-методы (*_api) - прямой вызов gRPC
- Высокоуровневые методы-обёртки - удобные для использования в тестах
"""

from grpc import Channel

from clients.grpc.client import GRPCClient
from clients.grpc.gateway.client import build_gateway_grpc_client
from contracts.services.gateway.cards.rpc_issue_virtual_card_pb2 import (
    IssueVirtualCardRequest,
    IssueVirtualCardResponse
)
from contracts.services.gateway.cards.rpc_issue_physical_card_pb2 import (
    IssuePhysicalCardRequest,
    IssuePhysicalCardResponse
)
from contracts.services.gateway.cards.cards_gateway_service_pb2_grpc import (
    CardsGatewayServiceStub
)


class CardsGatewayGRPCClient(GRPCClient):
    """
    gRPC-клиент для взаимодействия с CardsGatewayService.

    Предоставляет методы для выпуска виртуальных и физических карт.

    Examples:
        >>> # Создание клиента через билдер
        >>> client = build_cards_gateway_grpc_client()
        >>>
        >>> # Выпуск виртуальной карты
        >>> virtual_card = client.issue_virtual_card(
        ...     user_id="123e4567-e89b-12d3-a456-426614174000",
        ...     account_id="987fcdeb-51a2-43d7-9abc-123456789000"
        ... )
        >>> print(f"Virtual card ID: {virtual_card.card.id}")
        >>>
        >>> # Выпуск физической карты
        >>> physical_card = client.issue_physical_card(
        ...     user_id="123e4567-e89b-12d3-a456-426614174000",
        ...     account_id="987fcdeb-51a2-43d7-9abc-123456789000"
        ... )
        >>> print(f"Physical card ID: {physical_card.card.id}")
    """

    def __init__(self, channel: Channel):
        """
        Инициализация клиента для CardsGatewayService.

        Args:
            channel: gRPC-канал для подключения к сервису
        """
        super().__init__(channel)

        # gRPC-стаб, сгенерированный из .proto файла
        # Содержит методы IssueVirtualCard, IssuePhysicalCard и другие
        self._stub = CardsGatewayServiceStub(channel)

    # ==================== Низкоуровневые API-методы ====================

    def issue_virtual_card_api(
            self,
            request: IssueVirtualCardRequest
    ) -> IssueVirtualCardResponse:
        """
        Низкоуровневый вызов метода IssueVirtualCard через gRPC.

        Args:
            request: IssueVirtualCardRequest с данными для выпуска виртуальной карты
                    (user_id, account_id)

        Returns:
            IssueVirtualCardResponse с данными выпущенной виртуальной карты

        Example:
            >>> request = IssueVirtualCardRequest(
            ...     user_id="123e4567-e89b-12d3-a456-426614174000",
            ...     account_id="987fcdeb-51a2-43d7-9abc-123456789000"
            ... )
            >>> response = client.issue_virtual_card_api(request)
            >>> print(response.card.card_number)
        """
        return self._stub.IssueVirtualCard(request)

    def issue_physical_card_api(
            self,
            request: IssuePhysicalCardRequest
    ) -> IssuePhysicalCardResponse:
        """
        Низкоуровневый вызов метода IssuePhysicalCard через gRPC.

        Args:
            request: IssuePhysicalCardRequest с данными для выпуска физической карты
                    (user_id, account_id)

        Returns:
            IssuePhysicalCardResponse с данными выпущенной физической карты

        Example:
            >>> request = IssuePhysicalCardRequest(
            ...     user_id="123e4567-e89b-12d3-a456-426614174000",
            ...     account_id="987fcdeb-51a2-43d7-9abc-123456789000"
            ... )
            >>> response = client.issue_physical_card_api(request)
            >>> print(response.card.card_number)
        """
        return self._stub.IssuePhysicalCard(request)

    # ==================== Высокоуровневые методы-обёртки ====================

    def issue_virtual_card(
            self,
            user_id: str,
            account_id: str
    ) -> IssueVirtualCardResponse:
        """
        Выпуск виртуальной карты для указанного пользователя и счёта.

        Удобная обёртка над issue_virtual_card_api, которая самостоятельно
        формирует объект запроса.

        Args:
            user_id: Идентификатор пользователя (UUID)
            account_id: Идентификатор счёта (UUID)

        Returns:
            IssueVirtualCardResponse с данными выпущенной виртуальной карты

        Example:
            >>> response = client.issue_virtual_card(
            ...     user_id="123e4567-e89b-12d3-a456-426614174000",
            ...     account_id="987fcdeb-51a2-43d7-9abc-123456789000"
            ... )
            >>> print(f"Card ID: {response.card.id}")
            >>> print(f"Card number: {response.card.card_number}")
            >>> print(f"CVV: {response.card.cvv}")
            >>> print(f"PIN: {response.card.pin}")
        """
        request = IssueVirtualCardRequest(
            user_id=user_id,
            account_id=account_id
        )
        return self.issue_virtual_card_api(request)

    def issue_physical_card(
            self,
            user_id: str,
            account_id: str
    ) -> IssuePhysicalCardResponse:
        """
        Выпуск физической карты для указанного пользователя и счёта.

        Удобная обёртка над issue_physical_card_api, которая самостоятельно
        формирует объект запроса.

        Args:
            user_id: Идентификатор пользователя (UUID)
            account_id: Идентификатор счёта (UUID)

        Returns:
            IssuePhysicalCardResponse с данными выпущенной физической карты

        Example:
            >>> response = client.issue_physical_card(
            ...     user_id="123e4567-e89b-12d3-a456-426614174000",
            ...     account_id="987fcdeb-51a2-43d7-9abc-123456789000"
            ... )
            >>> print(f"Card ID: {response.card.id}")
            >>> print(f"Card number: {response.card.card_number}")
            >>> print(f"Cardholder: {response.card.card_holder}")
        """
        request = IssuePhysicalCardRequest(
            user_id=user_id,
            account_id=account_id
        )
        return self.issue_physical_card_api(request)


# ==================== Фабричная функция (Билдер) ====================

def build_cards_gateway_grpc_client() -> CardsGatewayGRPCClient:
    """
    Фабричная функция для создания экземпляра CardsGatewayGRPCClient.

    Скрывает детали создания gRPC-канала и инициализации клиента.

    Returns:
        CardsGatewayGRPCClient: Инициализированный клиент для CardsGatewayService

    Example:
        >>> client = build_cards_gateway_grpc_client()
        >>> virtual_card = client.issue_virtual_card(
        ...     user_id="123e4567-e89b-12d3-a456-426614174000",
        ...     account_id="987fcdeb-51a2-43d7-9abc-123456789000"
        ... )
    """
    # Создаём канал к grpc-gateway через существующий билдер
    channel = build_gateway_grpc_client()

    # Возвращаем готовый экземпляр клиента
    return CardsGatewayGRPCClient(channel=channel)

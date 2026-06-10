"""Модуль gRPC-клиента для CardsGatewayService."""

from clients.grpc.gateway.cards.client import (
    CardsGatewayGRPCClient,
    build_cards_gateway_grpc_client
)

__all__ = [
    "CardsGatewayGRPCClient",
    "build_cards_gateway_grpc_client"
]
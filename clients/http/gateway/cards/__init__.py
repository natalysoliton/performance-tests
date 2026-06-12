"""Клиенты для работы с API карт."""
from .client import CardsGatewayHTTPClient, VirtualCardRequest, PhysicalCardRequest

__all__ = [
    'CardsGatewayHTTPClient',
    'VirtualCardRequest',
    'PhysicalCardRequest'
]
#from .client import CardsGatewayHTTPClient, build_cards_gateway_http_client, build_cards_gateway_locust_http_client
from ..users import VirtualCardRequest, PhysicalCardRequest

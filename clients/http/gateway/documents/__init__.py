"""Клиенты для работы с API документов."""
from .client import (
    DocumentsGatewayHTTPClient,
    DocumentDict,
    GetTariffDocumentResponseDict,
    GetContractDocumentResponseDict,
    GetTariffDocumentQuery,
    GetContractDocumentQuery,
)

__all__ = [
    'DocumentsGatewayHTTPClient',
    'DocumentDict',
    'GetTariffDocumentResponseDict',
    'GetContractDocumentResponseDict',
    'GetTariffDocumentQuery',
    'GetContractDocumentQuery',
]
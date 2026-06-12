from grpc import Channel
from locust.env import Environment

from clients.grpc.client import GRPCClient
from clients.grpc.gateway.client import (
    build_gateway_grpc_client,
    build_gateway_locust_grpc_client
)
from contracts.services.gateway.documents.documents_gateway_service_pb2_grpc import DocumentsGatewayServiceStub
from contracts.services.gateway.documents.rpc_get_contract_document_pb2 import (
    GetContractDocumentRequest,
    GetContractDocumentResponse
)
from contracts.services.gateway.documents.rpc_get_tariff_document_pb2 import (
    GetTariffDocumentRequest,
    GetTariffDocumentResponse
)


class DocumentsGatewayGRPCClient(GRPCClient):
    """
    gRPC-клиент для взаимодействия с DocumentsGatewayService.
    """
    # ... (весь существующий код класса) ...


def build_documents_gateway_grpc_client() -> DocumentsGatewayGRPCClient:
    """
    Фабрика для создания экземпляра DocumentsGatewayGRPCClient.

    :return: Инициализированный клиент для DocumentsGatewayService.
    """
    return DocumentsGatewayGRPCClient(channel=build_gateway_grpc_client())


def build_documents_gateway_locust_grpc_client(environment: Environment) -> DocumentsGatewayGRPCClient:
    """
    Фабричная функция для создания экземпляра DocumentsGatewayGRPCClient,
    адаптированного для нагрузочного тестирования с Locust.

    :param environment: Объект окружения Locust
    :return: Экземпляр DocumentsGatewayGRPCClient со встроенным сбором метрик
    """
    channel = build_gateway_locust_grpc_client(environment)
    return DocumentsGatewayGRPCClient(channel=channel)
"""Модуль gRPC-клиента для OperationsGatewayService."""

from clients.grpc.gateway.operations.client import (
    OperationsGatewayGRPCClient,
    build_operations_gateway_grpc_client
)

__all__ = [
    "OperationsGatewayGRPCClient",
    "build_operations_gateway_grpc_client"
]
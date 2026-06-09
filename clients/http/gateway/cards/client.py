"""
HTTP-клиент для взаимодействия с /api/v1/cards сервиса http-gateway.
Использует Pydantic-модели для валидации запросов и ответов.
"""

from httpx import Response

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client
from clients.http.gateway.cards.schema import (
    IssueVirtualCardRequestSchema,
    IssueVirtualCardResponseSchema,
    IssuePhysicalCardRequestSchema,
    IssuePhysicalCardResponseSchema
)


class CardsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/cards сервиса http-gateway.

    Предоставляет методы для работы с картами:
    - Выпуск виртуальных карт
    - Выпуск физических карт
    """

    def issue_virtual_card_api(self, request: IssueVirtualCardRequestSchema) -> Response:
        """
        Выпуск виртуальной карты (низкоуровневый метод).

        :param request: Pydantic-модель с данными для выпуска виртуальной карты.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post(
            "/api/v1/cards/issue-virtual-card",
            json=request.model_dump(by_alias=True)
        )

    def issue_physical_card_api(self, request: IssuePhysicalCardRequestSchema) -> Response:
        """
        Выпуск физической карты (низкоуровневый метод).

        :param request: Pydantic-модель с данными для выпуска физической карты.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post(
            "/api/v1/cards/issue-physical-card",
            json=request.model_dump(by_alias=True)
        )

    def issue_virtual_card(self, user_id: str, account_id: str) -> IssueVirtualCardResponseSchema:
        """
        Выпуск виртуальной карты (высокоуровневый метод).

        Создает запрос, отправляет его и возвращает ответ в виде Pydantic-модели.

        :param user_id: ID пользователя, которому выпускается карта.
        :param account_id: ID счета, к которому привязывается карта.
        :return: Pydantic-модель с данными выпущенной виртуальной карты.
        """
        request = IssueVirtualCardRequestSchema(user_id=user_id, account_id=account_id)
        response = self.issue_virtual_card_api(request)
        return IssueVirtualCardResponseSchema.model_validate_json(response.text)

    def issue_physical_card(self, user_id: str, account_id: str) -> IssuePhysicalCardResponseSchema:
        """
        Выпуск физической карты (высокоуровневый метод).

        Создает запрос, отправляет его и возвращает ответ в виде Pydantic-модели.

        :param user_id: ID пользователя, которому выпускается карта.
        :param account_id: ID счета, к которому привязывается карта.
        :return: Pydantic-модель с данными выпущенной физической карты.
        """
        request = IssuePhysicalCardRequestSchema(user_id=user_id, account_id=account_id)
        response = self.issue_physical_card_api(request)
        return IssuePhysicalCardResponseSchema.model_validate_json(response.text)


def build_cards_gateway_http_client() -> CardsGatewayHTTPClient:
    """
    Функция создаёт экземпляр CardsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию CardsGatewayHTTPClient.
    """
    return CardsGatewayHTTPClient(client=build_gateway_http_client())
import time
import httpx

create_user_payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}
create_user_response = httpx.post("http://localhost:8003/api/v1/users", json=create_user_payload)
create_user_response_data = create_user_response.json()

open_credit_card_account_payload = {
    "userId": create_user_response_data["user"]["id"]
}
open_credit_card_account_response = httpx.post(
    "http://localhost:8003/api/v1/accounts/open-credit-card-account",
    json=open_credit_card_account_payload
)
open_credit_card_account_response_data = open_credit_card_account_response.json()

make_purchase_operation_payload = {
    "status": "IN_PROGRESS",
    "amount": 77.99,
    "cardId": open_credit_card_account_response_data["account"]["cards"][0]["id"],
    "category": "taxi",
    "accountId": open_credit_card_account_response_data["account"]["id"]
}
make_purchase_operation_response = httpx.post(
    "http://localhost:8003/api/v1/operations/make-purchase-operation",
    json=make_purchase_operation_payload
)
make_purchase_operation_response_data = make_purchase_operation_response.json()

get_operation_receipt_response = httpx.get(
    f"http://localhost:8003/api/v1/operations/operation-receipt/"
    f"{make_purchase_operation_response_data['operation']['id']}"
)
get_operation_receipt_response_data = get_operation_receipt_response.json()

print('Get operation receipt response:', get_operation_receipt_response_data)
print('Get operation receipt status code:', get_operation_receipt_response.status_code)

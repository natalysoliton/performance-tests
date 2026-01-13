import httpx
import time
import json

BASE_URL = "http://localhost:8003"


def run_workflow():
    """Основной поток выполнения."""

    # 1. Создать пользователя
    email = f"user_{int(time.time())}@bank.com"
    user_resp = httpx.post(
        f"{BASE_URL}/api/v1/users",
        json={"email": email, "firstName": "Ivan", "lastName": "Petrov"},
        timeout=10
    )
    user_resp.raise_for_status()
    user_id = user_resp.json()["id"]
    print(f"User created: {user_id}")

    # 2. Создать кредитный счёт
    credit_resp = httpx.post(
        f"{BASE_URL}/api/v1/accounts/open-credit-card-account",
        json={"userId": user_id, "creditLimit": 50000, "currency": "RUB"},
        timeout=10
    )
    credit_resp.raise_for_status()
    credit_data = credit_resp.json()
    account_id = credit_data["account"]["id"]
    card_id = credit_data["cards"][0]["id"]
    print(f"Account: {account_id}, Card: {card_id}")

    # 3. Совершить покупку
    purchase_resp = httpx.post(
        f"{BASE_URL}/api/v1/operations/make-purchase-operation",
        json={
            "status": "IN_PROGRESS",
            "amount": 77.99,
            "category": "taxi",
            "cardId": card_id,
            "accountId": account_id
        },
        timeout=10
    )
    purchase_resp.raise_for_status()
    operation_id = purchase_resp.json()["operationId"]
    print(f"Purchase operation: {operation_id}")

    # 4. Получить чек
    receipt_resp = httpx.get(
        f"{BASE_URL}/api/v1/operations/operation-receipt/{operation_id}",
        timeout=10
    )
    receipt_resp.raise_for_status()
    receipt_data = receipt_resp.json()

    # 5. Вывести результат
    print(f"\nStatus: {receipt_resp.status_code}")
    print("Receipt JSON:")
    print(json.dumps(receipt_data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    try:
        run_workflow()
    except Exception as e:
        print(f"Error: {e}")

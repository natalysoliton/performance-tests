import httpx
import time
import json

BASE_URL = "http://localhost:8003"


def create_user():
    """Создание пользователя и возврат его ID."""
    email = f"user_{int(time.time())}@example.com"
    payload = {
        "email": email,
        "firstName": "Test",
        "lastName": "User",
        "phone": "+79991234567"
    }

    resp = httpx.post(f"{BASE_URL}/api/v1/users", json=payload, timeout=10)
    resp.raise_for_status()

    user_data = resp.json()
    return user_data["id"]


def create_deposit_account(user_id):
    """Создание депозитного счёта для пользователя."""
    payload = {
        "userId": user_id,
        "currency": "RUB",
        "initialDeposit": 1000.0
    }

    resp = httpx.post(
        f"{BASE_URL}/api/v1/accounts/open-deposit-account",
        json=payload,
        timeout=10
    )

    return resp


def main():
    try:
        # 1. Создать пользователя
        user_id = create_user()
        print(f"Создан пользователь с ID: {user_id}")

        # 2. Создать депозитный счёт
        response = create_deposit_account(user_id)

        # 3. Вывести результат
        print(f"\nСтатус-код: {response.status_code}")
        print("\nJSON-ответ:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

    except httpx.HTTPStatusError as e:
        print(f"HTTP ошибка: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
    
from locust import HttpUser, between, task
from tools.fakers import fake


class OpenDebitCardAccountScenarioUser(HttpUser):
    """
    Виртуальный пользователь, который:
    1. При старте создаёт нового пользователя
    2. В рамках нагрузочной задачи открывает для него дебетовый счёт
    """
    # Пауза между задачами (имитация реального поведения)
    wait_time = between(1, 3)

    # Сохраняем ID созданного пользователя
    user_id: int = None

    def on_start(self) -> None:
        """
        Выполняется один раз при запуске каждого виртуального пользователя.
        Создаём нового пользователя через API.
        """
        # Генерируем данные пользователя с помощью faker
        request_body = {
            "email": fake.email(),
            "lastName": fake.last_name(),
            "firstName": fake.first_name(),
            "middleName": fake.middle_name(),
            "phoneNumber": fake.phone_number()
        }

        # Отправляем POST-запрос на создание пользователя
        with self.client.post(
                "/api/v1/users",
                json=request_body,
                catch_response=True,
                name="/api/v1/users (create)"
        ) as response:
            if response.status_code == 201:
                # Сохраняем user_id из ответа сервера
                response_data = response.json()
                self.user_id = response_data["user"]["id"]
                response.success()
            else:
                response.failure(f"Failed to create user: {response.status_code}")
                # Прерываем выполнение этого пользователя, так как без user_id нельзя открыть счёт
                self.environment.runner.quit()

    @task
    def open_debit_card_account(self):
        """
        Основная нагрузочная задача: открытие дебетового счёта.
        Отправляем POST-запрос с user_id, полученным при создании пользователя.
        """
        if self.user_id is None:
            # Если пользователь не создан, пропускаем задачу
            return

        request_body = {
            "userId": self.user_id
        }

        # Отправляем запрос на открытие счёта
        # Явно указываем name для группировки всех таких запросов в статистике
        self.client.post(
            "/api/v1/accounts/open-debit-card-account",
            json=request_body,
            name="/api/v1/accounts/open-debit-card-account"
        )
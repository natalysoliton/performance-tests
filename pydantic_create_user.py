from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    """
    Модель данных пользователя.

    Используется для представления полной информации о пользователе,
    включая уникальный идентификатор.

    Attributes:
        id: Уникальный идентификатор пользователя (строка)
        email: Адрес электронной почты пользователя (валидируется как EmailStr)
        last_name: Фамилия пользователя (snake_case в коде, но API ожидает lastName)
        first_name: Имя пользователя (snake_case в коде, но API ожидает firstName)
        middle_name: Отчество пользователя (snake_case в коде, но API ожидает middleName)
        phone_number: Номер телефона пользователя (snake_case в коде, но API ожидает phoneNumber)
    """

    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")


class CreateUserRequestSchema(BaseModel):
    """
    Модель запроса на создание пользователя.

    Используется для валидации входящих данных при POST-запросе
    на эндпоинт /api/v1/users. Содержит все поля, необходимые
    для создания нового пользователя (без id, который генерируется
    на стороне сервера).

    Attributes:
        email: Адрес электронной почты пользователя (обязательное поле)
        last_name: Фамилия пользователя
        first_name: Имя пользователя
        middle_name: Отчество пользователя
        phone_number: Номер телефона пользователя
    """

    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")


class CreateUserResponseSchema(BaseModel):
    """
    Модель ответа на создание пользователя.

    Используется для валидации ответа сервера при успешном создании
    пользователя. Содержит вложенную модель UserSchema с данными
    созданного пользователя.

    Attributes:
        user: Объект пользователя (вложенная модель UserSchema)
    """

    user: UserSchema


# Пример использования (для тестирования)
if __name__ == "__main__":
    # Пример создания запроса через словарь (camelCase от API)
    request_data = {
        "email": "john.doe@example.com",
        "lastName": "Doe",
        "firstName": "John",
        "middleName": "Michael",
        "phoneNumber": "+1234567890"
    }

    # Валидация запроса
    request = CreateUserRequestSchema(**request_data)
    print("Request validated successfully:")
    print(f"   Email: {request.email}")
    print(f"   Name: {request.first_name} {request.last_name}")
    print()

    # Симуляция ответа от сервера
    response_data = {
        "user": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "john.doe@example.com",
            "lastName": "Doe",
            "firstName": "John",
            "middleName": "Michael",
            "phoneNumber": "+1234567890"
        }
    }

    # Валидация ответа
    response = CreateUserResponseSchema(**response_data)
    print("Response validated successfully:")
    print(f"   User ID: {response.user.id}")
    print(f"   User email: {response.user.email}")
    print()

    # Демонстрация преобразования в JSON с camelCase (для отправки в API)
    print("Request as JSON (for API):")
    print(request.model_dump(by_alias=True, exclude_none=True))
    print()

    # Демонстрация работы с моделью в Python-стиле (snake_case)
    print("Working with model in Python style:")
    print(f"   request.first_name = {request.first_name}")
    print(f"   request.last_name = {request.last_name}")

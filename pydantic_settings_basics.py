# Импортируем необходимые типы из Pydantic
from pydantic import BaseModel, SecretStr, EmailStr, HttpUrl
import os
# Импортируем базовый класс настроек и конфигурацию из pydantic-settings
from pydantic_settings import BaseSettings, SettingsConfigDict

config_file = os.getenv("CONFIG_FILE", ".env.local")
# Вложенная модель для описания конфигурации тестового пользователя
class TestUserConfig(BaseModel):
    email: EmailStr  # Email с автоматической валидацией формата
    password: SecretStr  # Пароль, который будет скрыт при выводе (безопасность)


# Основная модель конфигурации проекта
class Settings(BaseSettings):
    # Специальный класс-конфигурация, указывающий источники и поведение загрузки
    base_url: str
    db_dsn: str

    model_config = SettingsConfigDict(env_file=config_file)


# При запуске скрипта создаётся объект с подгруженными значениями и выводится
print(Settings())

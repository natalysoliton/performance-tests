import locust.stats  # Модуль Locust, отвечающий за сбор и хранение статистики
from pydantic_settings import BaseSettings, SettingsConfigDict

from tools.config.grpc import GRPCClientConfig
from tools.config.http import HTTPClientConfig
from tools.config.locust import LocustUserConfig

# Настройка списка процентилей, которые будут попадать в отчёты Locust
locust.stats.PERCENTILES_TO_REPORT = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99, 1.0]

# Интервал (в секундах) между записями агрегированной статистики в CSV
locust.stats.CSV_STATS_INTERVAL_SEC = 5

# Интервал (в секундах) между записями "исторической" статистики (динамика значений)
locust.stats.HISTORY_STATS_INTERVAL_SEC = 5

# Интервал (в секундах) между обновлением статистики в консоли Locust
locust.stats.CONSOLE_STATS_INTERVAL_SEC = 5

# Интервал (в секундах) между принудительной записью CSV на диск
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 5

# Остальной код без изменений

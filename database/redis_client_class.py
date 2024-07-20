import redis
from typing import Optional, Union


class RedisClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client: Optional[redis.Redis] = None

    def connect(self):
        try:
            self.client = redis.Redis(host=self.host, port=self.port, decode_responses=True)
            self.client.ping()
            print('успешно подключились к редису')
        except redis.ConnectionError as e:
            print(f"Ошибка подключения к БД: {e}")
            self.client = None

    def set(self, key: str, value: float):
        if self.client:
            self.client.set(key, value)

    def get(self, key: str) -> Optional[float]:
        if self.client:
            result = self.client.get(key)
            if result is not None:
                try:
                    return float(result)
                except ValueError:
                    print(f"Ошибка преобразования значения '{result}' в float.")
                    return None
        return None

    def get_rates(self) -> str:
        if not self.client:
            return "Ошибка подключения к Redis"
        rates = self.client.scan_iter(match='*')
        rates_list = [f"Валюта {key} : {self.client.get(key)}" for key in rates]

        if not rates_list:
            return "Нет доступных данных по валютам."

        return "\n".join(rates_list)

    def get_exchange(self, val_1: str, val_2: str, ex_count: Union[int, float]) -> str:
        if val_1 == 'RUB':
            val_2_rate = self.get(val_2)
            if val_2_rate is None:
                return f"Курс для валюты {val_2} не найден"
            expr = float(ex_count) / val_2_rate
        elif val_2 == 'RUB':
            val_1_rate = self.get(val_1)
            if val_1_rate is None:
                return f"Курс для валюты {val_1} не найден"
            expr = val_1_rate * float(ex_count)
        else:
            return "Неподдерживаемые валюты"
        return f"{expr}"

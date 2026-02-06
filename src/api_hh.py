from abc import ABC, abstractmethod
import requests
from typing import Any, List, Dict


class HeadHunterAPIBase(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями
    """

    def __init__(self) -> None:
        """
        Инициализация HTTP-сессию для запроса к API
        """
        self.session = requests.Session()

    @abstractmethod
    def get_vacancy(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """
        Абстрактный метод для получения данных
        по заданному поиску
        """
        pass

    def _request(self, endpoint: str, params: Dict[str, Any]):
        """
            Выполняет HTTP-запросы  к API сервиса
        """
        self.url = f"{endpoint}"
        try:
            response = self.session.get(self.url, params=params)

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict):
                    return data
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка сети: {e}")
            return None
        except Exception as e:
            print(f"Ошибка: {e}")




class HeadHunterAPI(HeadHunterAPIBase):
    """
        Класс для работы с API HeadHunter
    """
    def __init__(self) -> None:
        super().__init__()

    def get_vacancy(self, query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        params = {
            "text": query,
            "area": kwargs.get("area", 1),
            "per_page": kwargs.get("per_page", 100),

        }
        all_vacancies = []
        page = 0

        while True:
            params["page"] = page
            data = self._request("https://api.hh.ru/vacancies", params=params)

            if not data:
                break

            items = data["items"]

            all_vacancies.extend(items)

            page += 1

        return all_vacancies


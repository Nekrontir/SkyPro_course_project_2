import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from src.vacancy import Vacancy


class VacancySaver(ABC):
    """
    Абстрактный класс для сохранения вакансий.
    Определяет интерфейс для работы с хранилищами.
    """

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавить вакансию в хранилище."""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """Получить вакансии по критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удалить вакансию из хранилища."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очистить хранилище."""
        pass


class JSONSaver(VacancySaver):
    """
    Класс для сохранения вакансий в JSON-файл.
    """

    def __init__(self, filename: str = "data/vacancies.json") -> None:
        """
        Инициализация JSON-сохранителя.

        Args:
            filename: Имя файла для сохранения
        """
        self._filename = filename
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Создает директорию для файла, если она не существует."""
        Path(self._filename).parent.mkdir(parents=True, exist_ok=True)

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """Загружает вакансии из файла."""
        if not os.path.exists(self._filename):
            return []

        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return cast(List[Dict[str, Any]], data)
                return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Сохраняет вакансии в файл."""
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в JSON-файл."""
        vacancies = self._load_vacancies()
        vacancy_dict = vacancy.to_dict()

        # Проверка на дубликаты
        if not any(v["id"] == vacancy.id for v in vacancies):
            vacancies.append(vacancy_dict)
            self._save_vacancies(vacancies)

    def add_vacancies(self, vacancies: List[Vacancy]) -> None:
        """Добавляет несколько вакансий."""
        for vacancy in vacancies:
            self.add_vacancy(vacancy)

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """Получает вакансии по критериям."""
        vacancies_data = self._load_vacancies()
        vacancies = [Vacancy.from_dict(v) for v in vacancies_data]

        if not criteria:
            return vacancies

        filtered_vacancies: List[Vacancy] = []
        for vacancy in vacancies:
            matches = True

            for key, value in criteria.items():
                if key == "keyword" and value:
                    keyword = value.lower()
                    vacancy_name = vacancy.name.lower() if vacancy.name else ""
                    vacancy_req = vacancy.requirements.lower() if vacancy.requirements else ""

                    if not (keyword in vacancy_name or keyword in vacancy_req):
                        matches = False
                        break

                elif key == "salary_from" and value:
                    if vacancy.salary_from < value:
                        matches = False
                        break

                elif key == "salary_to" and value:
                    if vacancy.salary_to > value:
                        matches = False
                        break

            if matches:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из JSON-файла."""
        vacancies = self._load_vacancies()
        vacancies = [v for v in vacancies if v["id"] != vacancy.id]
        self._save_vacancies(vacancies)

    def clear(self) -> None:
        """Очищает файл с вакансиями."""
        self._save_vacancies([])


class CSVSaver(VacancySaver):
    """Класс для сохранения вакансий в CSV-файл."""

    def __init__(self, filename: str = "data/vacancies.csv") -> None:
        self._filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в CSV-файл."""
        pass

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """Получает вакансии из CSV-файла."""
        return []

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из CSV-файла."""
        pass

    def clear(self) -> None:
        """Очищает CSV-файл с вакансиями."""
        pass


class TXTSaver(VacancySaver):
    """Класс для сохранения вакансий в TXT-файл."""

    def __init__(self, filename: str = "data/vacancies.txt") -> None:
        self._filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в TXT-файл."""
        pass

    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Vacancy]:
        """Получает вакансии из TXT-файла."""
        return []

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из TXT-файла."""
        pass

    def clear(self) -> None:
        """Очищает TXT-файл с вакансиями."""
        pass

import hashlib
import re
from typing import Any, Dict, List, Optional


class Vacancy:
    """
    Класс для представления вакансии.
    Поддерживает сравнение вакансий по зарплате.
    """

    __slots__ = (
        "_id",
        "_name",
        "_url",
        "_salary_from",
        "_salary_to",
        "_currency",
        "_description",
        "_requirements",
        "_employer",
    )

    def __init__(
        self,
        name: str,
        url: str,
        salary_from: Optional[int] = None,
        salary_to: Optional[int] = None,
        currency: Optional[str] = None,
        description: Optional[str] = None,
        requirements: Optional[str] = None,
        employer: Optional[str] = None,
    ):
        """
        Инициализация вакансии.

        Args:
            name: Название вакансии
            url: Ссылка на вакансию
            salary_from: Нижняя граница зарплаты
            salary_to: Верхняя граница зарплаты
            currency: Валюта зарплаты
            description: Описание вакансии
            requirements: Требования к кандидату
            employer: Название работодателя
        """
        self._name = name
        self._url = url
        self._salary_from = salary_from
        self._salary_to = salary_to
        self._currency = currency
        self._description = description
        self._requirements = requirements
        self._employer = employer
        self._id = self._generate_id()

        self._validate_salary()
        self._clean_text_fields()

    def _generate_id(self) -> str:
        """Генерация уникального ID на основе названия и URL."""
        data = f"{self._name}{self._url}"
        return hashlib.md5(data.encode()).hexdigest()

    def _validate_salary(self) -> None:
        """Валидация данных о зарплате."""
        if self._salary_from is None and self._salary_to is None:
            self._salary_from = 0
            self._salary_to = 0
            self._currency = "Зарплата не указана"
        elif self._salary_from is None:
            self._salary_from = self._salary_to if self._salary_to is not None else 0
        elif self._salary_to is None:
            self._salary_to = self._salary_from if self._salary_from is not None else 0

    def _clean_text_fields(self) -> None:
        """Очистка текстовых полей от HTML-тегов."""
        if self._description:
            self._description = self._remove_html_tags(self._description)
        if self._requirements:
            self._requirements = self._remove_html_tags(self._requirements)

    @staticmethod
    def _remove_html_tags(text: str) -> str:
        """Удаление HTML-тегов из текста."""
        clean = re.compile("<.*?>")
        return re.sub(clean, "", text)

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary_from(self) -> int:
        """Возвращает нижнюю границу зарплаты или 0 если не указана."""
        return self._salary_from or 0

    @property
    def salary_to(self) -> int:
        """Возвращает верхнюю границу зарплаты или 0 если не указана."""
        return self._salary_to or 0

    @property
    def currency(self) -> Optional[str]:
        return self._currency

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def requirements(self) -> Optional[str]:
        return self._requirements

    @property
    def employer(self) -> Optional[str]:
        return self._employer

    @property
    def avg_salary(self) -> float:
        """Возвращает среднюю зарплату."""
        if self.salary_from == 0 and self.salary_to == 0:
            return 0.0
        return (self.salary_from + self.salary_to) / 2.0

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary < other.avg_salary

    def __le__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary > other.avg_salary

    def __ge__(self, other: Any) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary >= other.avg_salary

    def __repr__(self) -> str:
        """Строковое представление вакансии."""
        salary_info: str
        if self.salary_from == 0 and self.salary_to == 0:
            salary_info = "Зарплата не указана"
        else:
            salary_info = f"{self.salary_from:,} - {self.salary_to:,} {self.currency or ''}"

        return (
            f"Вакансия: {self._name}\n"
            f"Компания: {self._employer or 'Не указано'}\n"
            f"Зарплата: {salary_info}\n"
            f"Требования: {(self._requirements[:100] + '...') if self._requirements and len(self._requirements) > 100 else self._requirements or ''}\n"
            f"Ссылка: {self._url}\n"
        )

    def __str__(self) -> str:
        """Пользовательское строковое представление."""
        return self.__repr__()

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict[str, Any]]) -> List["Vacancy"]:
        """
        Преобразует список словарей с данными о вакансиях в список объектов Vacancy.

        Args:
            vacancies_data: Список словарей с данными от API

        Returns:
            Список объектов Vacancy
        """
        vacancies: List[Vacancy] = []
        for item in vacancies_data:
            salary = item.get("salary")
            salary_from: Optional[int] = salary.get("from") if salary else None
            salary_to: Optional[int] = salary.get("to") if salary else None
            currency: Optional[str] = salary.get("currency") if salary else None

            snippet = item.get("snippet", {})
            description: Optional[str] = snippet.get("responsibility", "") or None
            requirements: Optional[str] = snippet.get("requirement", "") or None

            vacancy = cls(
                name=item.get("name", "Не указано"),
                url=item.get("alternate_url", ""),
                salary_from=salary_from,
                salary_to=salary_to,
                currency=currency,
                description=description,
                requirements=requirements,
                employer=item.get("employer", {}).get("name", "Не указано"),
            )
            vacancies.append(vacancy)

        return vacancies

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект вакансии в словарь."""
        return {
            "id": self._id,
            "name": self._name,
            "url": self._url,
            "salary_from": self._salary_from,
            "salary_to": self._salary_to,
            "currency": self._currency,
            "description": self._description,
            "requirements": self._requirements,
            "employer": self._employer,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        """Создает объект вакансии из словаря."""
        return cls(
            name=data["name"],
            url=data["url"],
            salary_from=data["salary_from"],
            salary_to=data["salary_to"],
            currency=data["currency"],
            description=data["description"],
            requirements=data["requirements"],
            employer=data["employer"],
        )

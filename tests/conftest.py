from pathlib import Path
from typing import Any, Dict, List

import pytest

from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancy_data() -> Dict[str, Any]:
    """Фикстура с тестовыми данными вакансии."""
    return {
        "name": "Python Developer",
        "url": "https://hh.ru/vacancy/12345678",
        "salary_from": 100000,
        "salary_to": 150000,
        "currency": "RUR",
        "description": "Разработка на Python",
        "requirements": "Опыт работы от 3 лет, знание Django",
        "employer": "ООО Технологии",
    }


@pytest.fixture
def sample_vacancy(sample_vacancy_data: Dict[str, Any]) -> Vacancy:
    """Фикстура с объектом вакансии."""
    return Vacancy(**sample_vacancy_data)


@pytest.fixture
def sample_vacancy_no_salary() -> Vacancy:
    """Фикстура с вакансией без зарплаты."""
    return Vacancy(
        name="Python Developer",
        url="https://hh.ru/vacancy/87654321",
        description="Разработка на Python",
        requirements="Опыт работы от 3 лет",
        employer="ООО Технологии",
    )


@pytest.fixture
def sample_vacancy_list() -> List[Vacancy]:
    """Фикстура со списком вакансий с разными именами."""
    vacancy1 = Vacancy(
        name="Python Developer A",
        url="https://hh.ru/vacancy/11111111",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        requirements="Опыт работы от 3 лет, знание Django",
        employer="ООО Технологии A",
    )

    vacancy2 = Vacancy(
        name="Python Developer B",
        url="https://hh.ru/vacancy/22222222",
        salary_from=80000,
        salary_to=120000,
        currency="RUR",
        requirements="Опыт работы от 2 лет, знание Flask",
        employer="ООО Технологии B",
    )

    vacancy3 = Vacancy(
        name="Senior Python Developer",
        url="https://hh.ru/vacancy/33333333",
        salary_from=200000,
        salary_to=300000,
        currency="RUR",
        requirements="Опыт работы от 5 лет, знание AWS",
        employer="ООО Технологии C",
    )

    return [vacancy1, vacancy2, vacancy3]


@pytest.fixture
def sample_api_response() -> List[Dict[str, Any]]:
    """Фикстура с ответом от API HH.ru."""
    return [
        {
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/12345678",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {
                "responsibility": "Разработка на Python",
                "requirement": "Опыт работы от 3 лет, знание Django",
            },
            "employer": {"name": "ООО Технологии"},
        },
        {
            "name": "Java Developer",
            "alternate_url": "https://hh.ru/vacancy/87654321",
            "salary": None,
            "snippet": {"responsibility": "Разработка на Java", "requirement": "Опыт работы от 2 лет"},
            "employer": {"name": "ООО Программы"},
        },
    ]


@pytest.fixture
def temp_json_file(tmp_path: Path) -> Path:
    """Фикстура для временного JSON-файла."""
    return tmp_path / "test_vacancies.json"

from typing import List

import pytest

from src.utils import filter_vacancies, get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.vacancy import Vacancy


class TestFilterVacancies:
    """Тесты для функции filter_vacancies."""

    def test_filter_vacancies_empty_filter(self, sample_vacancy_list: List[Vacancy]) -> None:
        """Тест фильтрации с пустым списком ключевых слов."""
        filtered = filter_vacancies(sample_vacancy_list, [])

        assert filtered == sample_vacancy_list
        assert len(filtered) == 3

    def test_filter_vacancies_single_keyword(self, sample_vacancy_list: List[Vacancy]) -> None:
        """Тест фильтрации по одному ключевому слову."""
        filtered = filter_vacancies(sample_vacancy_list, ["Senior"])

        assert len(filtered) == 1
        assert filtered[0].name == "Senior Python Developer"

    def test_filter_vacancies_multiple_keywords(self, sample_vacancy_list: List[Vacancy]) -> None:
        """Тест фильтрации по нескольким ключевым словам."""
        filtered = filter_vacancies(sample_vacancy_list, ["Python", "Developer"])

        assert len(filtered) == 3  # Все вакансии

        filtered = filter_vacancies(sample_vacancy_list, ["Java"])

        assert len(filtered) == 0  # Нет вакансий с Java

    def test_filter_vacancies_case_insensitive(self, sample_vacancy_list: List[Vacancy]) -> None:
        """Тест фильтрации без учета регистра."""
        filtered = filter_vacancies(sample_vacancy_list, ["senior"])

        assert len(filtered) == 1
        assert "Senior" in filtered[0].name

    def test_filter_vacancies_in_description(self) -> None:
        """Тест фильтрации по тексту в описании."""
        vacancy1 = Vacancy(name="Developer", url="url1", requirements="Знание Python и Django")
        vacancy2 = Vacancy(name="Developer", url="url2", requirements="Знание Java и Spring")

        vacancies = [vacancy1, vacancy2]
        filtered = filter_vacancies(vacancies, ["Django"])

        assert len(filtered) == 1
        assert filtered[0] == vacancy1


class TestGetVacanciesBySalary:
    """Тесты для функции get_vacancies_by_salary."""

    def test_get_vacancies_by_salary_no_filter(self, sample_vacancy_list: List[Vacancy]) -> None:
        """Тест фильтрации по зарплате без указания диапазона."""
        filtered = get_vacancies_by_salary(sample_vacancy_list, None)

        assert filtered == sample_vacancy_list

    def test_get_vacancies_by_salary_empty_range(self, sample_vacancy_list: List[Vacancy]) -> None:
        """Тест фильтрации по зарплате с пустым диапазоном."""
        filtered = get_vacancies_by_salary(sample_vacancy_list, "")

        assert filtered == sample_vacancy_list

    def test_get_vacancies_by_salary_single_value(self) -> None:
        """Тест фильтрации по минимальной зарплате."""
        vacancy1 = Vacancy("Dev1", "url1", 100000, 150000)
        vacancy2 = Vacancy("Dev2", "url2", 80000, 120000)
        vacancy3 = Vacancy("Dev3", "url3", 50000, 70000)

        vacancies = [vacancy1, vacancy2, vacancy3]

        filtered = get_vacancies_by_salary(vacancies, "90000")

        assert len(filtered) == 2
        assert vacancy1 in filtered
        assert vacancy2 in filtered
        assert vacancy3 not in filtered

    def test_get_vacancies_by_salary_range(self) -> None:
        """Тест фильтрации по диапазону зарплат."""
        vacancy1 = Vacancy("Dev1", "url1", 100000, 150000)
        vacancy2 = Vacancy("Dev2", "url2", 80000, 120000)
        vacancy3 = Vacancy("Dev3", "url3", 50000, 70000)

        vacancies = [vacancy1, vacancy2, vacancy3]
        filtered = get_vacancies_by_salary(vacancies, "90000-130000")

        assert len(filtered) == 2
        assert vacancy1 in filtered
        assert vacancy2 in filtered
        assert vacancy3 not in filtered

    def test_get_vacancies_by_salary_no_salary_vacancies(self) -> None:
        """Тест фильтрации вакансий без указанной зарплаты."""
        vacancy1 = Vacancy("Dev1", "url1", 100000, 150000)  # avg = 125000
        vacancy2 = Vacancy("Dev2", "url2")  # Без зарплаты, avg = 0
        vacancy3 = Vacancy("Dev3", "url3", 50000, 70000)  # avg = 60000

        vacancies = [vacancy1, vacancy2, vacancy3]

        filtered = get_vacancies_by_salary(vacancies, "60000")

        assert len(filtered) == 2
        assert vacancy1 in filtered
        assert vacancy2 not in filtered
        assert vacancy3 in filtered

    def test_get_vacancies_by_salary_invalid_range(self, sample_vacancy_list: List[Vacancy]) -> None:
        """Тест фильтрации по невалидному диапазону зарплат."""
        filtered = get_vacancies_by_salary(sample_vacancy_list, "invalid-range")

        assert filtered == sample_vacancy_list


class TestSortVacancies:
    """Тесты для функции sort_vacancies."""

    def test_sort_vacancies_descending(self) -> None:
        """Тест сортировки вакансий по убыванию зарплаты."""
        vacancy1 = Vacancy("Dev1", "url1", 100000, 150000)  # avg 125000
        vacancy2 = Vacancy("Dev2", "url2", 80000, 120000)  # avg 100000
        vacancy3 = Vacancy("Dev3", "url3", 200000, 250000)  # avg 225000

        vacancies = [vacancy1, vacancy2, vacancy3]
        sorted_vacancies = sort_vacancies(vacancies)

        assert sorted_vacancies[0] == vacancy3  # Самая высокая зарплата
        assert sorted_vacancies[1] == vacancy1
        assert sorted_vacancies[2] == vacancy2  # Самая низкая зарплата

    def test_sort_vacancies_with_no_salary(self) -> None:
        """Тест сортировки вакансий без зарплаты."""
        vacancy1 = Vacancy("Dev1", "url1", 100000, 150000)  # avg 125000
        vacancy2 = Vacancy("Dev2", "url2")  # Без зарплаты, avg 0
        vacancy3 = Vacancy("Dev3", "url3", 200000, 250000)  # avg 225000

        vacancies = [vacancy1, vacancy2, vacancy3]
        sorted_vacancies = sort_vacancies(vacancies)

        assert sorted_vacancies[0] == vacancy3  # Самая высокая
        assert sorted_vacancies[1] == vacancy1
        assert sorted_vacancies[2] == vacancy2  # Без зарплаты - в конце

    def test_sort_vacancies_empty_list(self) -> None:
        """Тест сортировки пустого списка."""
        sorted_vacancies = sort_vacancies([])

        assert sorted_vacancies == []

    def test_sort_vacancies_single_element(self) -> None:
        """Тест сортировки списка с одним элементом."""
        vacancy = Vacancy("Dev", "url", 100000, 150000)
        sorted_vacancies = sort_vacancies([vacancy])

        assert sorted_vacancies == [vacancy]


class TestGetTopVacancies:
    """Тесты для функции get_top_vacancies."""

    def test_get_top_vacancies_normal(self) -> None:
        """Тест получения топ N вакансий."""
        vacancies = [
            Vacancy("Dev1", "url1", 100000, 150000),
            Vacancy("Dev2", "url2", 80000, 120000),
            Vacancy("Dev3", "url3", 200000, 250000),
        ]

        top = get_top_vacancies(vacancies, 2)

        assert len(top) == 2
        assert top[0].avg_salary > top[1].avg_salary

    def test_get_top_vacancies_more_than_available(self) -> None:
        """Тест получения топ N, когда N больше количества вакансий."""
        vacancies = [Vacancy("Dev1", "url1", 100000, 150000), Vacancy("Dev2", "url2", 80000, 120000)]

        top = get_top_vacancies(vacancies, 5)

        assert len(top) == 2

    def test_get_top_vacancies_zero_or_negative(self) -> None:
        """Тест получения топ 0 или отрицательного числа."""
        vacancies = [Vacancy("Dev1", "url1", 100000, 150000), Vacancy("Dev2", "url2", 80000, 120000)]

        # top_n = 0
        top = get_top_vacancies(vacancies, 0)
        assert top == vacancies

        # top_n = -1
        top = get_top_vacancies(vacancies, -1)
        assert top == vacancies

    def test_get_top_vacancies_empty_list(self) -> None:
        """Тест получения топ N из пустого списка."""
        top = get_top_vacancies([], 5)

        assert top == []


class TestPrintVacancies:
    """Тесты для функции print_vacancies."""

    def test_print_vacancies_empty_list(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест вывода пустого списка вакансий."""
        print_vacancies([])

        captured = capsys.readouterr()
        assert "По вашему запросу вакансий не найдено" in captured.out

    def test_print_vacancies_with_data(
        self, sample_vacancy_list: List[Vacancy], capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест вывода списка вакансий."""
        print_vacancies(sample_vacancy_list[:2])

        captured = capsys.readouterr()
        output = captured.out

        assert "Найдено вакансий: 2" in output
        assert "Python Developer A" in output
        assert "Python Developer B" in output
        assert "ООО Технологии A" in output
        assert "ООО Технологии B" in output
        assert "100,000 - 150,000" in output
        assert "80,000 - 120,000" in output
        assert "Опыт работы от 3 лет" in output
        assert "Опыт работы от 2 лет" in output
        assert "=" * 80 in output
        assert "-" * 80 in output
        assert "Зарплата не указана" not in output

    def test_print_vacancies_truncated_requirements(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест вывода вакансии с обрезанными требованиями."""
        long_requirements = "Требование " * 30
        vacancy = Vacancy(name="Developer", url="url", requirements=long_requirements)

        print_vacancies([vacancy])

        captured = capsys.readouterr()
        output = captured.out

        assert "..." in output
        assert len(output) < len(long_requirements) + 500

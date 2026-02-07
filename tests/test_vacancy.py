from typing import Any, Dict, List

from src.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy."""

    def test_vacancy_creation(self, sample_vacancy_data: Dict[str, Any]) -> None:
        """Тест создания объекта вакансии."""
        vacancy = Vacancy(**sample_vacancy_data)

        assert vacancy.name == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/12345678"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.currency == "RUR"
        assert vacancy.description == "Разработка на Python"
        assert vacancy.requirements == "Опыт работы от 3 лет, знание Django"
        assert vacancy.employer == "ООО Технологии"
        assert isinstance(vacancy.id, str)
        assert len(vacancy.id) == 32

    def test_vacancy_creation_no_salary(self, sample_vacancy_no_salary: Vacancy) -> None:
        """Тест создания вакансии без зарплаты."""
        assert sample_vacancy_no_salary.name == "Python Developer"
        assert sample_vacancy_no_salary.salary_from == 0
        assert sample_vacancy_no_salary.salary_to == 0
        assert sample_vacancy_no_salary.currency == "Зарплата не указана"

    def test_vacancy_creation_partial_salary(self) -> None:
        """Тест создания вакансии с частично указанной зарплатой."""
        vacancy1 = Vacancy(name="Developer", url="https://hh.ru/test1", salary_from=100000)
        assert vacancy1.salary_from == 100000
        assert vacancy1.salary_to == 100000

        vacancy2 = Vacancy(name="Developer", url="https://hh.ru/test2", salary_to=150000)
        assert vacancy2.salary_from == 150000
        assert vacancy2.salary_to == 150000

    def test_avg_salary(self, sample_vacancy: Vacancy, sample_vacancy_no_salary: Vacancy) -> None:
        """Тест расчета средней зарплаты."""
        assert sample_vacancy.avg_salary == 125000.0
        assert sample_vacancy_no_salary.avg_salary == 0.0

    def test_comparison_operators(self) -> None:
        """Тест операторов сравнения вакансий по зарплате."""
        vacancy1 = Vacancy("Dev1", "url1", 100000, 150000)
        vacancy2 = Vacancy("Dev2", "url2", 80000, 120000)
        vacancy3 = Vacancy("Dev3", "url3", 100000, 150000)

        assert vacancy1 > vacancy2
        assert vacancy2 < vacancy1
        assert vacancy1 >= vacancy3
        assert vacancy1 <= vacancy3
        assert vacancy1 == vacancy3
        assert vacancy1 != vacancy2

    def test_to_dict(self, sample_vacancy: Vacancy) -> None:
        """Тест преобразования вакансии в словарь."""
        vacancy_dict = sample_vacancy.to_dict()

        assert isinstance(vacancy_dict, dict)
        assert vacancy_dict["name"] == "Python Developer"
        assert vacancy_dict["salary_from"] == 100000
        assert vacancy_dict["salary_to"] == 150000
        assert "id" in vacancy_dict

    def test_from_dict(self, sample_vacancy_data: Dict[str, Any]) -> None:
        """Тест создания вакансии из словаря."""
        vacancy_dict = {**sample_vacancy_data, "id": "test_id_123"}
        vacancy = Vacancy.from_dict(vacancy_dict)

        assert vacancy.name == vacancy_dict["name"]
        assert vacancy.url == vacancy_dict["url"]
        assert vacancy.salary_from == vacancy_dict["salary_from"]

    def test_cast_to_object_list(self, sample_api_response: List[Dict[str, Any]]) -> None:
        """Тест преобразования данных API в список объектов Vacancy."""
        vacancies = Vacancy.cast_to_object_list(sample_api_response)

        assert len(vacancies) == 2
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].name == "Python Developer"
        assert vacancies[0].salary_from == 100000
        assert vacancies[1].name == "Java Developer"
        assert vacancies[1].salary_from == 0

    def test_remove_html_tags(self) -> None:
        """Тест удаления HTML-тегов из текста."""
        html_text = "<p>Hello <strong>World</strong></p> <br> Test"
        clean_text = Vacancy._remove_html_tags(html_text)

        assert clean_text == "Hello World  Test"
        assert "<" not in clean_text
        assert ">" not in clean_text

    def test_repr_string(self, sample_vacancy: Vacancy) -> None:
        """Тест строкового представления вакансии."""
        repr_str = repr(sample_vacancy)

        assert "Python Developer" in repr_str
        assert "ООО Технологии" in repr_str
        assert "100,000 - 150,000" in repr_str
        assert "RUR" in repr_str
        assert "https://hh.ru/vacancy/12345678" in repr_str

    def test_slots(self) -> None:
        """Тест использования __slots__ для экономии памяти."""
        vacancy = Vacancy("Test", "url")

        assert hasattr(vacancy, "__slots__")
        assert not hasattr(vacancy, "__dict__")

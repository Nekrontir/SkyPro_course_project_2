import json
from pathlib import Path
from src.saver import JSONSaver, CSVSaver, TXTSaver, VacancySaver
from src.vacancy import Vacancy

class TestVacancySaver:
    """Тесты для абстрактного класса VacancySaver."""

    def test_abstract_methods_exist(self) -> None:
        """Тест, что абстрактные методы определены."""
        assert hasattr(VacancySaver, 'add_vacancy')
        assert hasattr(VacancySaver, 'get_vacancies')
        assert hasattr(VacancySaver, 'delete_vacancy')
        assert hasattr(VacancySaver, 'clear')



class TestJSONSaver:
    """Тесты для класса JSONSaver."""

    def test_init_default_filename(self) -> None:
        """Тест инициализации с именем файла по умолчанию."""
        saver = JSONSaver()
        assert saver._filename == "data/vacancies.json"

    def test_init_custom_filename(self) -> None:
        """Тест инициализации с пользовательским именем файла."""
        saver = JSONSaver("custom.json")
        assert saver._filename == "custom.json"

    def test_add_vacancy(self, temp_json_file: Path, sample_vacancy: Vacancy) -> None:
        """Тест добавления вакансии в файл."""
        saver = JSONSaver(str(temp_json_file))

        saver.add_vacancy(sample_vacancy)

        assert temp_json_file.exists()

        with open(temp_json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["name"] == "Python Developer"
        assert data[0]["id"] == sample_vacancy.id

    def test_add_vacancy_no_duplicates(
            self,
            temp_json_file: Path,
            sample_vacancy: Vacancy
    ) -> None:
        """Тест, что дубликаты вакансий не добавляются."""
        saver = JSONSaver(str(temp_json_file))

        saver.add_vacancy(sample_vacancy)
        saver.add_vacancy(sample_vacancy)

        with open(temp_json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == 1

    def test_add_vacancies(
            self,
            temp_json_file: Path,
            sample_vacancy_list: list
    ) -> None:
        """Тест добавления нескольких вакансий."""
        saver = JSONSaver(str(temp_json_file))

        saver.add_vacancies(sample_vacancy_list)

        with open(temp_json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert len(data) == len(sample_vacancy_list)

    def test_get_vacancies_empty(self, temp_json_file: Path) -> None:
        """Тест получения вакансий из пустого файла."""
        saver = JSONSaver(str(temp_json_file))

        vacancies = saver.get_vacancies()

        assert vacancies == []

    def test_get_vacancies_with_data(
            self,
            temp_json_file: Path,
            sample_vacancy: Vacancy
    ) -> None:
        """Тест получения вакансий из файла с данными."""
        saver = JSONSaver(str(temp_json_file))
        saver.add_vacancy(sample_vacancy)

        vacancies = saver.get_vacancies()

        assert len(vacancies) == 1
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].name == "Python Developer"

    def test_get_vacancies_with_keyword_filter(
            self,
            temp_json_file: Path,
            sample_vacancy_list: list
    ) -> None:
        """Тест фильтрации вакансий по ключевому слову."""
        saver = JSONSaver(str(temp_json_file))
        saver.add_vacancies(sample_vacancy_list)

        filtered = saver.get_vacancies({"keyword": "Senior"})

        assert len(filtered) == 1
        assert filtered[0].name == "Senior Python Developer"

        filtered = saver.get_vacancies({"keyword": "Python"})

        assert len(filtered) == 3

    def test_get_vacancies_with_salary_filter(
            self,
            temp_json_file: Path,
            sample_vacancy_list: list
    ) -> None:
        """Тест фильтрации вакансий по зарплате."""
        saver = JSONSaver(str(temp_json_file))
        saver.add_vacancies(sample_vacancy_list)

        filtered = saver.get_vacancies({"salary_from": 150000})

        assert len(filtered) == 1
        assert filtered[0].name == "Senior Python Developer"

        filtered = saver.get_vacancies({"salary_to": 120000})

        assert len(filtered) == 1

    def test_delete_vacancy(
            self,
            temp_json_file: Path
    ) -> None:
        """Тест удаления вакансии из файла."""
        # Создаем простые вакансии
        vacancy1 = Vacancy("Dev1", "url1", 100000, 150000)
        vacancy2 = Vacancy("Dev2", "url2", 80000, 120000)
        vacancy3 = Vacancy("Dev3", "url3", 200000, 250000)

        saver = JSONSaver(str(temp_json_file))
        saver.add_vacancy(vacancy1)
        saver.add_vacancy(vacancy2)
        saver.add_vacancy(vacancy3)
        saver.delete_vacancy(vacancy2)
        remaining = saver.get_vacancies()
        assert len(remaining) == 2
        remaining_names = {v.name for v in remaining}
        assert remaining_names == {"Dev1", "Dev3"}

    def test_clear(self, temp_json_file: Path, sample_vacancy: Vacancy) -> None:
        """Тест очистки файла с вакансиями."""
        saver = JSONSaver(str(temp_json_file))
        saver.add_vacancy(sample_vacancy)

        saver.clear()

        vacancies = saver.get_vacancies()

        assert vacancies == []

        with open(temp_json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert data == []

    def test_load_vacancies_file_not_exists(self, temp_json_file: Path) -> None:
        """Тест загрузки вакансий из несуществующего файла."""
        saver = JSONSaver(str(temp_json_file))

        vacancies = saver.get_vacancies()

        assert vacancies == []
        assert not temp_json_file.exists()

    def test_load_vacancies_invalid_json(self, temp_json_file: Path) -> None:
        """Тест загрузки вакансий из поврежденного JSON-файла."""
        with open(temp_json_file, 'w', encoding='utf-8') as f:
            f.write("invalid json {")

        saver = JSONSaver(str(temp_json_file))
        vacancies = saver.get_vacancies()

        assert vacancies == []


class TestOtherSavers:
    """Тесты для других классов сохранения (CSV, TXT)."""

    def test_csv_saver_init(self) -> None:
        """Тест инициализации CSVSaver."""
        saver = CSVSaver()
        assert saver._filename == "data/vacancies.csv"

    def test_csv_saver_methods_exist(self) -> None:
        """Тест, что методы CSVSaver существуют (заглушки)."""
        saver = CSVSaver()

        assert hasattr(saver, 'add_vacancy')
        assert hasattr(saver, 'get_vacancies')
        assert hasattr(saver, 'delete_vacancy')
        assert hasattr(saver, 'clear')

        vacancy = Vacancy("Test", "url")
        saver.add_vacancy(vacancy)
        assert saver.get_vacancies() == []
        saver.delete_vacancy(vacancy)
        saver.clear()

    def test_txt_saver_init(self) -> None:
        """Тест инициализации TXTSaver."""
        saver = TXTSaver()
        assert saver._filename == "data/vacancies.txt"

    def test_txt_saver_methods_exist(self) -> None:
        """Тест, что методы TXTSaver существуют (заглушки)."""
        saver = TXTSaver()

        assert hasattr(saver, 'add_vacancy')
        assert hasattr(saver, 'get_vacancies')
        assert hasattr(saver, 'delete_vacancy')
        assert hasattr(saver, 'clear')

        vacancy = Vacancy("Test", "url")
        saver.add_vacancy(vacancy)
        assert saver.get_vacancies() == []
        saver.delete_vacancy(vacancy)
        saver.clear()
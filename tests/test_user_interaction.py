from unittest.mock import Mock, patch

import pytest

from src.user_interaction import user_interaction
from src.vacancy import Vacancy


class TestUserInteraction:
    """Тесты для функции user_interaction (версия с меню)."""

    @patch("src.user_interaction.HeadHunterAPI")
    @patch("src.user_interaction.JSONSaver")
    def test_menu_option_1_search_vacancies(
        self, mock_json_saver_class: Mock, mock_api_class: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест пункта меню 1: Поиск вакансий."""
        mock_api = Mock()
        mock_api.get_vacancies.return_value = [{"test": "data"}]
        mock_api_class.return_value = mock_api

        mock_saver = Mock()
        mock_json_saver_class.return_value = mock_saver

        with patch("src.user_interaction.Vacancy.cast_to_object_list") as mock_cast:
            mock_vacancy = Mock()
            mock_cast.return_value = [mock_vacancy]

            inputs = [
                "1",
                "Python",
                "2",
                "50",
                "y",
                "y",
                "",
                "0",
            ]

            with (
                patch("builtins.input", side_effect=inputs),
                patch("src.user_interaction.print_vacancies") as mock_print,
            ):
                user_interaction()

                # Проверяем вызовы
                mock_api.get_vacancies.assert_called_once_with("Python", area=2, per_page=50)
                mock_saver.add_vacancies.assert_called_once_with([mock_vacancy])
                mock_print.assert_called_once()

    @patch("src.user_interaction.JSONSaver")
    def test_menu_option_2_show_saved(self, mock_json_saver_class: Mock, capsys: pytest.CaptureFixture[str]) -> None:
        """Тест пункта меню 2: Показать сохраненные вакансии."""
        mock_saver = Mock()
        mock_vacancy = Mock(spec=Vacancy)
        mock_vacancy.name = "Test Vacancy"
        mock_saver.get_vacancies.return_value = [mock_vacancy]
        mock_json_saver_class.return_value = mock_saver

        inputs = [
            "2",
            "",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs), patch("src.user_interaction.print_vacancies") as mock_print:
            user_interaction()

            mock_saver.get_vacancies.assert_called_once()
            mock_print.assert_called_once_with([mock_vacancy])

    @patch("src.user_interaction.JSONSaver")
    def test_menu_option_3_search_by_keyword(
        self, mock_json_saver_class: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест пункта меню 3: Поиск по ключевым словам."""
        mock_saver = Mock()
        mock_vacancy = Mock()
        mock_vacancy.name = "Python Developer"
        mock_saver.get_vacancies.return_value = [mock_vacancy]
        mock_json_saver_class.return_value = mock_saver

        inputs = [
            "3",
            "Python",
            "",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs), patch("src.user_interaction.print_vacancies") as mock_print:
            user_interaction()

            mock_saver.get_vacancies.assert_called_once_with({"keyword": "Python"})
            mock_print.assert_called_once_with([mock_vacancy])

    @patch("src.user_interaction.JSONSaver")
    @patch("src.user_interaction.sort_vacancies")
    @patch("src.user_interaction.get_top_vacancies")
    def test_menu_option_4_top_n_vacancies(
        self,
        mock_get_top_vacancies: Mock,
        mock_sort_vacancies: Mock,
        mock_json_saver_class: Mock,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Тест пункта меню 4: Топ N вакансий по зарплате."""
        mock_saver = Mock()
        mock_vacancy = Mock()
        mock_saver.get_vacancies.return_value = [mock_vacancy]
        mock_json_saver_class.return_value = mock_saver

        mock_sort_vacancies.return_value = [mock_vacancy]
        mock_get_top_vacancies.return_value = [mock_vacancy]

        inputs = [
            "4",
            "3",
            "",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs), patch("src.user_interaction.print_vacancies") as mock_print:
            user_interaction()

            mock_saver.get_vacancies.assert_called_once()
            mock_sort_vacancies.assert_called_once_with([mock_vacancy])
            mock_get_top_vacancies.assert_called_once_with([mock_vacancy], 3)
            mock_print.assert_called_once_with([mock_vacancy])

    @patch("src.user_interaction.JSONSaver")
    @patch("src.user_interaction.get_vacancies_by_salary")
    def test_menu_option_5_filter_by_salary(
        self, mock_get_vacancies_by_salary: Mock, mock_json_saver_class: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест пункта меню 5: Фильтрация по зарплате."""
        mock_saver = Mock()
        mock_vacancy = Mock()
        mock_saver.get_vacancies.return_value = [mock_vacancy]
        mock_json_saver_class.return_value = mock_saver

        mock_get_vacancies_by_salary.return_value = [mock_vacancy]

        inputs = [
            "5",
            "100000-150000",
            "",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs), patch("src.user_interaction.print_vacancies") as mock_print:
            user_interaction()

            mock_saver.get_vacancies.assert_called_once()
            mock_get_vacancies_by_salary.assert_called_once_with([mock_vacancy], "100000-150000")
            mock_print.assert_called_once_with([mock_vacancy])

    @patch("src.user_interaction.JSONSaver")
    def test_menu_option_6_clear_vacancies(
        self, mock_json_saver_class: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест пункта меню 6: Очистка вакансий."""
        mock_saver = Mock()
        mock_json_saver_class.return_value = mock_saver

        inputs = [
            "6",
            "y",
            "",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs):
            user_interaction()

            mock_saver.clear.assert_called_once()

    @patch("src.user_interaction.JSONSaver")
    def test_menu_option_6_clear_vacancies_cancel(
        self, mock_json_saver_class: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест пункта меню 6: Отмена очистки."""
        mock_saver = Mock()
        mock_json_saver_class.return_value = mock_saver

        inputs = [
            "6",
            "n",
            "",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs):
            user_interaction()

            mock_saver.clear.assert_not_called()

    @patch("src.user_interaction.HeadHunterAPI")
    @patch("src.user_interaction.JSONSaver")
    def test_menu_invalid_choice(
        self, mock_json_saver_class: Mock, mock_api_class: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест неверного выбора в меню."""
        mock_saver = Mock()
        mock_json_saver_class.return_value = mock_saver

        mock_api = Mock()
        mock_api_class.return_value = mock_api

        inputs = [
            "invalid",
            "",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs):
            user_interaction()

        captured = capsys.readouterr()
        assert "Неверный выбор" in captured.out

    @patch("src.user_interaction.HeadHunterAPI")
    @patch("src.user_interaction.JSONSaver")
    def test_menu_option_1_empty_query(
        self, mock_json_saver_class: Mock, mock_api_class: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест пункта 1 с пустым запросом."""
        mock_saver = Mock()
        mock_json_saver_class.return_value = mock_saver

        mock_api = Mock()
        mock_api_class.return_value = mock_api

        inputs = [
            "1",
            "",
            "Python",
            "",
            "",
            "n",
            "n",
            "",
            "0",
        ]

        with (
            patch("builtins.input", side_effect=inputs),
            patch("src.user_interaction.Vacancy.cast_to_object_list", return_value=[]),
        ):
            user_interaction()

        captured = capsys.readouterr()
        assert "Запрос не может быть пустым" in captured.out

    @patch("src.user_interaction.HeadHunterAPI")
    @patch("src.user_interaction.JSONSaver")
    def test_menu_option_1_api_error(
        self, mock_json_saver_class: Mock, mock_api_class: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест пункта 1 с ошибкой API."""
        mock_saver = Mock()
        mock_json_saver_class.return_value = mock_saver

        mock_api = Mock()
        mock_api.get_vacancies.side_effect = Exception("API Error")
        mock_api_class.return_value = mock_api

        inputs = [
            "1",
            "Python",
            "",
            "",
            "",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs):
            user_interaction()

        captured = capsys.readouterr()
        assert "Ошибка при получении вакансий" in captured.out

    @patch("src.user_interaction.HeadHunterAPI")
    @patch("src.user_interaction.JSONSaver")
    def test_menu_option_4_invalid_number(
        self, mock_json_saver_class: Mock, mock_api_class: Mock, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Тест пункта 4 с невалидным числом для топа."""
        mock_saver = Mock()
        mock_json_saver_class.return_value = mock_saver

        mock_api = Mock()
        mock_api_class.return_value = mock_api

        inputs = [
            "4",
            "invalid",
            "",
            "0",
        ]

        with patch("builtins.input", side_effect=inputs):
            user_interaction()

        captured = capsys.readouterr()
        assert "Некорректный ввод" in captured.out

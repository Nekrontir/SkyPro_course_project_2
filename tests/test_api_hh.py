from unittest.mock import Mock, patch

from src.api_hh import HeadHunterAPI, HeadHunterAPIBase


class TestHeadHunterAPIBase:
    """Тесты для абстрактного базового класса API."""

    def test_abstract_method_exists(self) -> None:
        """Тест, что абстрактный метод определен."""
        assert hasattr(HeadHunterAPIBase, "get_vacancies")


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI."""

    def test_init(self) -> None:
        """Тест инициализации класса."""
        api = HeadHunterAPI()
        assert api.session is not None
        assert api.BASE_URL == "https://api.hh.ru/vacancies"

    @patch("src.api_hh.requests.Session")
    def test_get_vacancies_success(self, mock_session_class: Mock) -> None:
        """Тест успешного получения вакансий."""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"id": "1", "name": "Python Developer"}, {"id": "2", "name": "Java Developer"}],
            "pages": 1,
        }
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        api = HeadHunterAPI()
        api.session = mock_session

        vacancies = api.get_vacancies("Python")

        assert len(vacancies) == 2
        assert vacancies[0]["name"] == "Python Developer"
        mock_session.get.assert_called_once()

        call_args = mock_session.get.call_args
        assert call_args[0][0] == "https://api.hh.ru/vacancies"
        assert call_args[1]["params"]["text"] == "Python"
        assert call_args[1]["params"]["area"] == 113
        assert call_args[1]["params"]["per_page"] == 100

    @patch("src.api_hh.requests.Session")
    def test_get_vacancies_with_kwargs(self, mock_session_class: Mock) -> None:
        """Тест получения вакансий с дополнительными параметрами."""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [], "pages": 1}
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        api = HeadHunterAPI()
        api.session = mock_session

        api.get_vacancies("Python", area=2, per_page=50, pages=2)

        call_args = mock_session.get.call_args
        params = call_args[1]["params"]

        assert params["area"] == 2
        assert params["per_page"] == 50
        assert params["page"] == 0

    @patch("src.api_hh.requests.Session")
    def test_get_vacancies_empty_response(self, mock_session_class: Mock) -> None:
        """Тест получения пустого ответа от API."""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [], "pages": 0}
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        api = HeadHunterAPI()
        api.session = mock_session

        vacancies = api.get_vacancies("Python")

        assert vacancies == []

    @patch("src.api_hh.requests.Session")
    def test_get_vacancies_network_error(self, mock_session_class: Mock) -> None:
        """Тест обработки сетевой ошибки."""
        mock_session = Mock()
        mock_session.get.side_effect = Exception("Network error")
        mock_session_class.return_value = mock_session

        api = HeadHunterAPI()
        api.session = mock_session

        vacancies = api.get_vacancies("Python")

        assert vacancies == []

    @patch("src.api_hh.requests.Session")
    def test_get_vacancies_multiple_pages(self, mock_session_class: Mock) -> None:
        """Тест получения вакансий с нескольких страниц."""
        mock_session = Mock()

        response1 = Mock()
        response1.status_code = 200
        response1.json.return_value = {"items": [{"id": "1", "name": "Dev1"}], "pages": 2}

        response2 = Mock()
        response2.status_code = 200
        response2.json.return_value = {"items": [{"id": "2", "name": "Dev2"}], "pages": 2}

        mock_session.get.side_effect = [response1, response2]
        mock_session_class.return_value = mock_session

        api = HeadHunterAPI()
        api.session = mock_session

        vacancies = api.get_vacancies("Python", pages=2)

        assert len(vacancies) == 2
        assert mock_session.get.call_count == 2

    def test_request_method_success(self) -> None:
        """Тест метода _request при успешном запросе."""
        api = HeadHunterAPI()

        with patch.object(api.session, "get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"test": "data"}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = api._request("https://test.com", {"param": "value"})

            assert result == {"test": "data"}
            mock_get.assert_called_once_with("https://test.com", params={"param": "value"}, timeout=10)

    def test_request_method_error(self) -> None:
        """Тест метода _request при ошибке."""
        api = HeadHunterAPI()

        with patch.object(api.session, "get") as mock_get:
            mock_get.side_effect = Exception("Test error")

            result = api._request("https://test.com", {})

            assert result is None

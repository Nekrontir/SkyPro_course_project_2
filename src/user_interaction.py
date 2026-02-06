from typing import Any, Dict

from src.api_hh import HeadHunterAPI
from src.saver import JSONSaver
from src.utils import get_top_vacancies, get_vacancies_by_salary, print_vacancies, sort_vacancies
from src.vacancy import Vacancy


def user_interaction() -> None:
    """
    Расширенная функция взаимодействия с пользователем через меню.
    """
    print("=" * 60)
    print("      ПРОГРАММА ДЛЯ ПОИСКА ВАКАНСИЙ НА HH.RU")
    print("=" * 60)

    hh_api = HeadHunterAPI()
    saver = JSONSaver()

    while True:
        print("\nМЕНЮ:")
        print("1. Найти вакансии на HH.ru")
        print("2. Показать сохраненные вакансии")
        print("3. Найти вакансии по ключевым словам")
        print("4. Вывести топ N вакансий по зарплате")
        print("5. Фильтровать вакансии по зарплате")
        print("6. Очистить сохраненные вакансии")
        print("0. Выход")

        choice = input("\nВыберите действие (0-6): ").strip()

        if choice == "0":
            print("Выход из программы. До свидания!")
            break

        elif choice == "1":
            search_query = input("Введите поисковый запрос (например: Python разработчик): ").strip()
            if not search_query:
                print("Запрос не может быть пустым!")
                continue

            area_input = input(
                "Введите код региона (1 - Москва, 2 - Санкт-Петербург, 113 - Россия, Enter для России): "
            ).strip()
            area: int = int(area_input) if area_input else 113

            per_page_input = input("Введите количество вакансий для загрузки (по умолчанию 100): ").strip()
            per_page: int = int(per_page_input) if per_page_input.isdigit() else 100

            print(f"\nИщем вакансии по запросу: '{search_query}'...")

            try:
                vacancies_data = hh_api.get_vacancies(search_query, area=area, per_page=per_page)
                vacancies = Vacancy.cast_to_object_list(vacancies_data)

                print(f"Найдено {len(vacancies)} вакансий")

                # Предлагаем сохранить
                save = input("Сохранить найденные вакансии? (y/n): ").strip().lower()
                if save == "y":
                    saver.add_vacancies(vacancies)
                    print(f"Сохранено {len(vacancies)} вакансий")

                show = input("Показать первые 10 вакансий? (y/n): ").strip().lower()
                if show == "y":
                    print_vacancies(vacancies[:10])

            except ValueError as e:
                print(f"Ошибка ввода: {e}")
            except Exception as e:
                print(f"Ошибка при получении вакансий: {e}")

        elif choice == "2":
            vacancies = saver.get_vacancies()
            if vacancies:
                print(f"\nСохранено вакансий: {len(vacancies)}")
                print_vacancies(vacancies)
            else:
                print("Нет сохраненных вакансий.")

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска: ").strip()
            if keyword:
                criteria: Dict[str, Any] = {"keyword": keyword}
                vacancies = saver.get_vacancies(criteria)
                print_vacancies(vacancies)
            else:
                print("Ключевое слово не может быть пустым.")

        elif choice == "4":
            try:
                top_n_input = input("Введите количество вакансий для топа (N): ").strip()
                top_n = int(top_n_input)
                if top_n <= 0:
                    print("Число должно быть положительным!")
                    continue

                vacancies = saver.get_vacancies()
                sorted_vacancies = sort_vacancies(vacancies)
                top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
                print_vacancies(top_vacancies)
            except ValueError:
                print("Некорректный ввод! Введите число.")

        elif choice == "5":
            try:
                salary_range = input("Введите диапазон зарплат (например: 100000-200000 или 150000): ").strip()
                vacancies = saver.get_vacancies()
                filtered = get_vacancies_by_salary(vacancies, salary_range)
                print_vacancies(filtered)
            except Exception as e:
                print(f"Ошибка при фильтрации: {e}")

        elif choice == "6":
            confirm = input("Вы уверены, что хотите очистить все сохраненные вакансии? (y/n): ").strip().lower()
            if confirm == "y":
                saver.clear()
                print("Все вакансии удалены.")

        else:
            print("Неверный выбор. Попробуйте снова.")

        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    user_interaction()

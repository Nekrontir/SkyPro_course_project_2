from typing import List, Optional

from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевым словам.

    Args:
        vacancies: Список вакансий
        filter_words: Список ключевых слов

    Returns:
        Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered: List[Vacancy] = []
    for vacancy in vacancies:
        text_parts: List[str] = []

        if vacancy.name:
            text_parts.append(vacancy.name.lower())
        if vacancy.requirements:
            text_parts.append(vacancy.requirements.lower())
        if vacancy.description:
            text_parts.append(vacancy.description.lower())

        text = " ".join(text_parts)

        if any(word.lower() in text for word in filter_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: Optional[str]) -> List[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат.

    Args:
        vacancies: Список вакансий
        salary_range: Строка диапазона зарплат, например "100000-150000"

    Returns:
        Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies

    try:
        if "-" in salary_range:
            salary_parts = salary_range.split("-")
            if len(salary_parts) == 2:
                salary_from, salary_to = map(int, salary_parts)
                filtered: List[Vacancy] = []
                for vacancy in vacancies:
                    vac_from = vacancy.salary_from
                    vac_to = vacancy.salary_to
                    if vac_from > 0 and vac_to > 0:
                        if vac_from >= salary_from and vac_to <= salary_to:
                            filtered.append(vacancy)
                return filtered
        else:
            salary_min = int(salary_range)
            filtered = []
            for vacancy in vacancies:
                if vacancy.avg_salary >= salary_min:
                    filtered.append(vacancy)
            return filtered
    except ValueError:
        return vacancies

    return vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортирует вакансии по убыванию зарплаты.

    Args:
        vacancies: Список вакансий

    Returns:
        Отсортированный список вакансий
    """
    return sorted(vacancies, key=lambda v: v.avg_salary, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий.

    Args:
        vacancies: Список вакансий
        top_n: Количество вакансий для возврата

    Returns:
        Список из top_n вакансий
    """
    return vacancies[:top_n] if top_n > 0 else vacancies


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Выводит вакансии в читаемом формате.

    Args:
        vacancies: Список вакансий для вывода
    """
    if not vacancies:
        print("\nПо вашему запросу вакансий не найдено.")
        return

    print(f"\nНайдено вакансий: {len(vacancies)}\n")
    print("=" * 80)

    for i, vacancy in enumerate(vacancies, 1):
        print(f"Вакансия #{i}")
        print(f"Название: {vacancy.name}")
        print(f"Компания: {vacancy.employer or 'Не указано'}")

        if vacancy.salary_from == 0 and vacancy.salary_to == 0:
            print("Зарплата: Не указана")
        else:
            salary_from = f"{vacancy.salary_from:,}" if vacancy.salary_from else "не указано"
            salary_to = f"{vacancy.salary_to:,}" if vacancy.salary_to else "не указано"
            currency = vacancy.currency if vacancy.currency else ""
            print(f"Зарплата: {salary_from} - {salary_to} {currency}")

        if vacancy.requirements:
            req = vacancy.requirements
            if len(req) > 200:
                req = req[:200] + "..."
            print(f"Требования: {req}")

        print(f"Ссылка: {vacancy.url}")
        print("-" * 80)

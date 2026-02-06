import os
import sys

from src.user_interaction import user_interaction

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    """
    Основная функция программы.
    """
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\nПроизошла непредвиденная ошибка: {e}")
        print("Пожалуйста, попробуйте снова или сообщите об ошибке.")
        sys.exit(1)


if __name__ == "__main__":
    main()

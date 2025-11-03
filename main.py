"""
Бот-асистент для управління адресною книгою.
Підтримує команди для додавання, зміни, видалення контактів та роботи з днями народження.
"""

from typing import Callable, List
from contact_book import AddressBook, Record


def input_error(func: Callable) -> Callable:
    """
    Декоратор для обробки помилок вводу користувача.
    
    Args:
        func: Функція-обробник команди
        
    Returns:
        Callable: Обгорнута функція з обробкою помилок
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Помилка значення: {e}"
        except IndexError:
            return "Недостатньо аргументів для команди."
        except KeyError as e:
            return f"Помилка ключа: {e}"
        except Exception as e:
            return f"Несподівана помилка: {e}"
    return inner


def parse_input(user_input: str) -> tuple[str, List[str]]:
    """
    Розбирає введений користувачем рядок на команду та аргументи.
    
    Args:
        user_input: Рядок введений користувачем
        
    Returns:
        tuple: Команда та список аргументів
    """
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args


@input_error
def add_contact(args: List[str], book: AddressBook) -> str:
    """
    Додає новий контакт або телефон до існуючого контакту.
    
    Args:
        args: Список аргументів [ім'я, телефон]
        book: Адресна книга
        
    Returns:
        str: Повідомлення про результат операції
    """
    if len(args) < 2:
        raise IndexError("Потрібно вказати ім'я та телефон.")
    
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    
    if phone:
        record.add_phone(phone)
    
    return message


@input_error
def change_contact(args: List[str], book: AddressBook) -> str:
    """
    Змінює телефон для існуючого контакту.
    
    Args:
        args: Список аргументів [ім'я, старий_телефон, новий_телефон]
        book: Адресна книга
        
    Returns:
        str: Повідомлення про результат операції
    """
    if len(args) < 3:
        raise IndexError("Потрібно вказати ім'я, старий телефон та новий телефон.")
    
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    
    if record is None:
        return f"Контакт {name} не знайдено."
    
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: List[str], book: AddressBook) -> str:
    """
    Показує телефони для вказаного контакту.
    
    Args:
        args: Список аргументів [ім'я]
        book: Адресна книга
        
    Returns:
        str: Телефони контакту або повідомлення про помилку
    """
    if len(args) < 1:
        raise IndexError("Потрібно вказати ім'я контакту.")
    
    name = args[0]
    record = book.find(name)
    
    if record is None:
        return f"Контакт {name} не знайдено."
    
    if not record.phones:
        return f"У контакту {name} немає телефонів."
    
    phones = "; ".join(phone.value for phone in record.phones)
    return f"{name}: {phones}"


@input_error
def show_all(book: AddressBook) -> str:
    """
    Показує всі контакти в адресній книзі.
    
    Args:
        book: Адресна книга
        
    Returns:
        str: Список всіх контактів або повідомлення про порожню книгу
    """
    if not book.data:
        return "Адресна книга порожня."
    
    result = []
    for record in book.data.values():
        result.append(str(record))
    
    return "\n".join(result)


@input_error
def add_birthday(args: List[str], book: AddressBook) -> str:
    """
    Додає дату народження до контакту.
    
    Args:
        args: Список аргументів [ім'я, дата_народження]
        book: Адресна книга
        
    Returns:
        str: Повідомлення про результат операції
    """
    if len(args) < 2:
        raise IndexError("Потрібно вказати ім'я та дату народження (DD.MM.YYYY).")
    
    name, birthday, *_ = args
    record = book.find(name)
    
    if record is None:
        return f"Контакт {name} не знайдено."
    
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: List[str], book: AddressBook) -> str:
    """
    Показує дату народження для вказаного контакту.
    
    Args:
        args: Список аргументів [ім'я]
        book: Адресна книга
        
    Returns:
        str: Дата народження або повідомлення про помилку
    """
    if len(args) < 1:
        raise IndexError("Потрібно вказати ім'я контакту.")
    
    name = args[0]
    record = book.find(name)
    
    if record is None:
        return f"Контакт {name} не знайдено."
    
    if record.birthday is None:
        return f"У контакту {name} не вказано дату народження."
    
    return f"{name}: {record.birthday.value}"


@input_error
def birthdays(args: List[str], book: AddressBook) -> str:
    """
    Показує дні народження, які відбудуться протягом наступного тижня.
    
    Args:
        args: Список аргументів (не використовується)
        book: Адресна книга
        
    Returns:
        str: Список днів народження або повідомлення про їх відсутність
    """
    upcoming = book.get_upcoming_birthdays()
    
    if not upcoming:
        return "Немає днів народження на наступному тижні."
    
    result = []
    for item in upcoming:
        result.append(f"{item['name']}: {item['congratulation_date']}")
    
    return "\n".join(result)


def show_help() -> str:
    """
    Показує список всіх доступних команд з описом та аргументами.
    
    Returns:
        str: Форматований список команд
    """
    help_text = """
Доступні команди:

  hello
    Отримати вітання від бота.
    Приклад: hello

  add [ім'я] [телефон]
    Додати новий контакт або телефон до існуючого контакту.
    Телефон повинен містити 10 цифр.
    Приклад: add John 1234567890

  change [ім'я] [старий телефон] [новий телефон]
    Змінити телефонний номер для існуючого контакту.
    Приклад: change John 1234567890 0987654321

  phone [ім'я]
    Показати всі телефонні номери для вказаного контакту.
    Приклад: phone John

  all
    Показати всі контакти в адресній книзі.
    Приклад: all

  add-birthday [ім'я] [дата народження]
    Додати дату народження для вказаного контакту.
    Формат дати: DD.MM.YYYY
    Приклад: add-birthday John 01.11.1990

  show-birthday [ім'я]
    Показати дату народження для вказаного контакту.
    Приклад: show-birthday John

  birthdays
    Показати дні народження, які відбудуться протягом наступного тижня.
    Приклад: birthdays

  help
    Показати цей список команд.
    Приклад: help

  close або exit
    Закрити програму.
    Приклад: exit
"""
    return help_text.strip()


def main() -> None:
    """
    Головна функція програми. Запускає цикл обробки команд користувача.
    """
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print("Type 'help' to see available commands.")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "help":
            print(show_help())

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

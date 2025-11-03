"""
Тестовий скрипт для перевірки функціональності бота.
"""

from contact_book import AddressBook
from main import (
    add_contact, 
    change_contact, 
    show_phone, 
    show_all, 
    add_birthday, 
    show_birthday, 
    birthdays,
    show_help
)


def test_bot():
    """Тестує основну функціональність бота."""
    print("=" * 50)
    print("Тестування бота-асистента")
    print("=" * 50)
    
    # Тест 0: Команда help
    print("\n0. Команда help:")
    print(show_help())
    
    # Створення адресної книги
    book = AddressBook()
    
    # Тест 1: Додавання контактів
    print("\n1. Додавання контактів:")
    print(add_contact(["John", "1234567890"], book))
    print(add_contact(["Jane", "0987654321"], book))
    print(add_contact(["John", "5555555555"], book))  # Додавання другого телефону
    
    # Тест 2: Показати всі контакти
    print("\n2. Всі контакти:")
    print(show_all(book))
    
    # Тест 3: Показати телефон
    print("\n3. Показати телефон John:")
    print(show_phone(["John"], book))
    
    # Тест 4: Зміна телефону
    print("\n4. Зміна телефону John:")
    print(change_contact(["John", "1234567890", "1112223333"], book))
    print(show_phone(["John"], book))
    
    # Тест 5: Додавання дати народження
    print("\n5. Додавання дат народження:")
    print(add_birthday(["John", "01.11.1990"], book))
    print(add_birthday(["Jane", "05.11.1985"], book))
    
    # Тест 6: Показати дату народження
    print("\n6. Показати дату народження John:")
    print(show_birthday(["John"], book))
    
    # Тест 7: Показати всі контакти з датами народження
    print("\n7. Всі контакти з датами народження:")
    print(show_all(book))
    
    # Тест 8: Показати найближчі дні народження
    print("\n8. Найближчі дні народження:")
    print(birthdays([], book))
    
    # Тест 9: Обробка помилок
    print("\n9. Тестування обробки помилок:")
    print("9.1. Неправильний формат телефону:")
    print(add_contact(["Test", "123"], book))
    
    print("\n9.2. Неправильний формат дати:")
    print(add_birthday(["John", "32.13.2000"], book))
    
    print("\n9.3. Контакт не знайдено:")
    print(show_phone(["Unknown"], book))
    
    print("\n9.4. Недостатньо аргументів:")
    print(add_contact(["OnlyName"], book))
    
    print("\n9.5. Порожнє ім'я:")
    print(add_contact(["", "1234567890"], book))
    
    print("\n9.6. Ім'я з пробілів:")
    print(add_contact(["   ", "1234567890"], book))
    
    print("\n" + "=" * 50)
    print("Тестування завершено!")
    print("=" * 50)


if __name__ == "__main__":
    test_bot()

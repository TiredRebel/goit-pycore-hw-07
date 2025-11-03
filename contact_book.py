from collections import UserDict
from datetime import datetime, timedelta
from typing import List, Optional


class Field:
    """Базовий клас для полів запису."""
    
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""
    
    def __init__(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Ім'я контакту не може бути порожнім.")
        super().__init__(value.strip())


class Phone(Field):
    """Клас для зберігання номера телефону. Має валідацію формату (10 цифр)."""
    
    def __init__(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен складатися з 10 цифр.")
        super().__init__(value)


class Birthday(Field):
    """Клас для зберігання дати народження. Формат: DD.MM.YYYY."""
    
    def __init__(self, value: str) -> None:
        try:
            # Перевірка коректності даних та перетворення рядка на об'єкт datetime
            self.date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів."""
    
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone_number: str) -> None:
        """Додавання телефону."""
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number: str) -> None:
        """Видалення телефону."""
        phone_to_remove = self.find_phone(phone_number)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Номер телефону не знайдено.")

    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        """Редагування телефону."""
        for i, p in enumerate(self.phones):
            if p.value == old_phone_number:
                self.phones[i] = Phone(new_phone_number)
                return
        raise ValueError("Номер телефону для редагування не знайдено.")

    def find_phone(self, phone_number: str) -> Optional[Phone]:
        """Пошук телефону."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday: str) -> None:
        """Додавання дня народження до контакту."""
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    """Клас для зберігання та управління записами."""
    
    def add_record(self, record: Record) -> None:
        """Додавання запису."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Пошук запису за ім'ям."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видалення запису за ім'ям."""
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Контакт не знайдено.")

    def get_upcoming_birthdays(self) -> List[dict]:
        """
        Повертає список користувачів, яких потрібно привітати на наступному тижні.
        
        Returns:
            List[dict]: Список словників з іменами та датами привітання
        """
        upcoming_birthdays = []
        today = datetime.today().date()
        
        for record in self.data.values():
            if record.birthday:
                # Отримуємо дату народження
                birthday_date = record.birthday.date.date()
                
                # Переносимо день народження на поточний рік
                birthday_this_year = birthday_date.replace(year=today.year)
                
                # Якщо день народження вже минув цього року, беремо наступний рік
                if birthday_this_year < today:
                    birthday_this_year = birthday_date.replace(year=today.year + 1)
                
                # Перевіряємо, чи день народження в найближчі 7 днів
                days_until_birthday = (birthday_this_year - today).days
                
                if 0 <= days_until_birthday <= 7:
                    # Перевіряємо, чи випадає на вихідні
                    congratulation_date = birthday_this_year
                    
                    # Якщо субота (5) або неділя (6), переносимо на понеділок
                    if birthday_this_year.weekday() == 5:  # Субота
                        congratulation_date = birthday_this_year + timedelta(days=2)
                    elif birthday_this_year.weekday() == 6:  # Неділя
                        congratulation_date = birthday_this_year + timedelta(days=1)
                    
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                    })
        
        return upcoming_birthdays


def main() -> None:
    """Головна функція програми."""
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    print("All records in the address book:")
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    if john:
        print("\nEditing John's phone...")
        john.edit_phone("1234567890", "1112223333")

        print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

        # Пошук конкретного телефону у записі John
        print("\nSearching for a specific phone in John's record:")
        found_phone = john.find_phone("5555555555")
        print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    print("\nDeleting Jane's record...")
    book.delete("Jane")
    
    print("\nAll records after deletion:")
    for name, record in book.data.items():
        print(record)


if __name__ == "__main__":
    main()

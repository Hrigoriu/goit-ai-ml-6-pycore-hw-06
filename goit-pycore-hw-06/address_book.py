
from collections import UserDict


class Field:
    """Базовий клас для всіх полів запису."""

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Клас для зберігання обов'язкового імені контакту."""

    def __init__(self, value: str) -> None:
        # Перевіряємо, що ім'я не порожнє.
        if not value.strip():
            raise ValueError("Name cannot be empty.")

        super().__init__(value.strip())


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією (має бути 10 цифр)."""

    def __init__(self, value: str) -> None:
        # Перевіряємо, що номер складається рівно з 10 цифр.
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits.")

        super().__init__(value)

    @staticmethod
    def validate(phone_number: str) -> bool:
        """Перевіряє формат номера телефону."""
        return len(phone_number) == 10 and phone_number.isdigit()


class Record:
    """Клас для зберігання інформації про один контакт."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone_number: str) -> None:
        """Додає новий номер телефону до контакту."""
        self.phones.append(Phone(phone_number))

    def find_phone(self, phone_number: str) -> Phone | None:
        """Шукає об'єкт Phone за номером телефону."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

        return None

    def remove_phone(self, phone_number: str) -> bool:
        """Видаляє номер телефону з контакту."""
        phone = self.find_phone(phone_number)

        if phone is None:
            return False

        self.phones.remove(phone)
        return True

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Замінює старий номер телефону на новий."""

        # Перевіряємо, чи існує старий номер.
        phone = self.find_phone(old_phone)

        if phone is None:
            raise ValueError(
                f"Phone number {old_phone} not found in this record."
            )

        # Перевіряємо новий номер до зміни даних.
        new_phone_object = Phone(new_phone)

        # Змінюємо значення знайденого об'єкта Phone.
        phone.value = new_phone_object.value

    def __str__(self) -> str:
        """Повертає текстове представлення контакту."""
        phones = "; ".join(phone.value for phone in self.phones)

        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    """Клас адресної книги для зберігання та управління контактами."""

    def add_record(self, record: Record) -> None:
        """Додає запис до адресної книги."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Знаходить запис за ім'ям контакту."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис з адресної книги."""
        self.data.pop(name, None)

    def __str__(self) -> str:
        """Повертає текстове представлення всієї адресної книги."""
        return "\n".join(
            str(record) for record in self.data.values()
        )


# Блок тестування функціональності адресної книги.
if __name__ == "__main__":

    # Створюємо нову адресну книгу.
    book = AddressBook()

    # Створюємо запис для John.
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додаємо запис John до адресної книги.
    book.add_record(john_record)

    # Створюємо та додаємо запис для Jane.
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виводимо всі записи адресної книги.
    print("--- Всі записи в книзі ---")
    print(book)

    # Знаходимо запис John та редагуємо його номер.
    john = book.find("John")

    if john is not None:
        john.edit_phone("1234567890", "1112223333")

        print("\n--- Запис John після редагування ---")
        print(john)

        # Шукаємо конкретний номер телефону.
        found_phone = john.find_phone("5555555555")

        print(f"\nЗнайдений телефон: {john.name}: {found_phone}")

        # Видаляємо один номер телефону.
        john.remove_phone("5555555555")

        print("\n--- John після видалення телефону ---")
        print(john)

    # Видаляємо запис Jane з адресної книги.
    book.delete("Jane")

    print("\n--- Книга після видалення Jane ---")
    print(book)

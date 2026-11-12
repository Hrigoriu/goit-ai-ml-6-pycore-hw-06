from address_book import AddressBook, Record, Phone, Name

def run_tests():
    """Комплексна перевірка роботи адресної книги."""

    print("=== ТЕСТУВАННЯ ADDRESS BOOK ===")

    # 1. Створення адресної книги.
    book = AddressBook()
    print("\n[1] Створення адресної книги: OK")

    # 2. Створення контакту та додавання телефонів.
    john = Record("John")
    john.add_phone("1234567890")
    john.add_phone("5555555555")
    book.add_record(john)

    print("\n[2] Додавання контакту:")
    print(book)

    # 3. Пошук контакту.
    assert book.find("John") is john
    assert book.find("Michael") is None
    print("\n[3] Пошук контакту: OK")

    # 4. Перевірка пошуку телефону.
    assert john.find_phone("1234567890") is not None
    assert john.find_phone("0000000000") is None
    print("[4] Пошук телефону: OK")

    # 5. Редагування телефону.
    john.edit_phone("1234567890", "1112223333")
    assert john.find_phone("1112223333") is not None
    assert john.find_phone("1234567890") is None
    print("[5] Редагування телефону: OK")

    # 6. Перевірка некоректного телефону.
    try:
        john.add_phone("12345")
    except ValueError:
        print("[6] Валідація телефону: OK")
    else:
        raise AssertionError("Некоректний телефон був прийнятий!")

    # 7. Перевірка помилки редагування.
    try:
        john.edit_phone("0000000000", "2223334444")
    except ValueError:
        print("[7] Обробка помилки редагування: OK")
    else:
        raise AssertionError("Очікувалася помилка ValueError!")

    # 8. Перевірка незмінності номера після невдалого редагування.
    assert john.find_phone("1112223333") is not None
    print("[8] Збереження старого номера: OK")

    # 9. Видалення телефону.
    assert john.remove_phone("1112223333") is True
    assert john.remove_phone("1112223333") is False
    print("[9] Видалення телефону: OK")

    # 10. Видалення контакту.
    book.delete("John")
    assert book.find("John") is None
    print("[10] Видалення контакту: OK")

    # 11. Видалення неіснуючого контакту.
    book.delete("Michael")
    print("[11] Видалення неіснуючого контакту: OK")

    print("\n=== ВСІ ТЕСТИ ПРОЙДЕНО ===")


if __name__ == "__main__":
    run_tests()
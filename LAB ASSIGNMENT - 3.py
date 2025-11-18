import json
from pathlib import Path
import logging

logging.basicConfig(filename='library_inventory.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class Book:
    def __init__(self, title, author, isbn, status='available'):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {self.status}"

    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn, "status": self.status}

    def issue(self):
        if self.status == 'available':
            self.status = 'issued'
            logging.info(f"Issued book {self.isbn}")
            return True
        return False

    def return_book(self):
        if self.status == 'issued':
            self.status = 'available'
            logging.info(f"Returned book {self.isbn}")
            return True
        return False

    def is_available(self):
        return self.status == 'available'


class LibraryInventory:
    def __init__(self, filepath='library_inventory.json'):
        self.filepath = Path(filepath)
        self.books = []
        self.load_books()

    def load_books(self):
        if self.filepath.exists():
            try:
                with self.filepath.open('r') as f:
                    books_data = json.load(f)
                    self.books = [Book(**book) for book in books_data]
                    logging.info("Loaded books from file")
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Error loading books: {e}")
                self.books = []
        else:
            self.books = []

    def save_books(self):
        try:
            with self.filepath.open('w') as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
            logging.info("Saved books to file")
        except IOError as e:
            logging.error(f"Error saving books: {e}")

    def add_book(self, book):
        if not any(b.isbn == book.isbn for b in self.books):
            self.books.append(book)
            self.save_books()
            logging.info(f"Added book {book.isbn}")
            return True
        logging.warning(f"Book with ISBN {book.isbn} already exists")
        return False

    def search_books(self, keyword):
        keyword_lower = keyword.lower()
        results = [book for book in self.books if keyword_lower in book.title.lower()
                   or keyword_lower in book.author.lower()
                   or keyword_lower in book.isbn.lower()]
        return results

    def list_books(self):
        return self.books

    def issue_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.issue():
                    self.save_books()
                    return True
                else:
                    return False
        return False

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                if book.return_book():
                    self.save_books()
                    return True
                else:
                    return False
        return False


def main():
    inventory = LibraryInventory()

    menu = """
Library Inventory Manager
1. Add Book
2. Search Books
3. List All Books
4. Issue Book
5. Return Book
6. Exit
Choose an option: """

    while True:
        choice = input(menu).strip()
        if choice == '1':
            title = input("Enter title: ").strip()
            author = input("Enter author: ").strip()
            isbn = input("Enter ISBN: ").strip()
            book = Book(title, author, isbn)
            if inventory.add_book(book):
                print("Book added successfully.")
            else:
                print("Book with this ISBN already exists.")
        elif choice == '2':
            keyword = input("Enter title/author/ISBN to search: ").strip()
            results = inventory.search_books(keyword)
            if results:
                for book in results:
                    print(book)
            else:
                print("No books found.")
        elif choice == '3':
            for book in inventory.list_books():
                print(book)
        elif choice == '4':
            isbn = input("Enter ISBN to issue: ").strip()
            if inventory.issue_book(isbn):
                print("Book issued successfully.")
            else:
                print("Book is not available or does not exist.")
        elif choice == '5':
            isbn = input("Enter ISBN to return: ").strip()
            if inventory.return_book(isbn):
                print("Book returned successfully.")
            else:
                print("Book was not issued or does not exist.")
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()

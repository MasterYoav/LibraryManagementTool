from typing import List, Dict
import csv
import os
import Book
import os
import csv
from BookFactory import BookFactory
from log_decorator import log_decorator


# --- Lending and Returning Books ---
class Library:
    def __init__(self, books_file="csv_files/books.csv"):
        self.books_file = books_file
        self.books = []  # List to store book objects
        self.load_books()

    def load_books(self):
        if os.path.exists(self.books_file):
            with open(self.books_file, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = BookFactory.create_book(
                        title=row["title"],
                        author=row["author"],
                        is_loaned=row["is_loaned"].lower() == "yes",
                        copies=int(row["copies"]),
                        genre=row["genre"],
                        year=int(row["year"])
                    )
                    self.books.append(book)

    def save_books(self):
        with open(self.books_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["title", "author", "is_loaned", "copies", "genre", "year"])
            writer.writeheader()
            for book in self.books:
                writer.writerow({
                    "title": book.title,
                    "author": book.author,
                    "is_loaned": "Yes" if book.is_loaned else "No",
                    "copies": book.copies,
                    "genre": book.genre,
                    "year": book.year
                })

    @log_decorator("Book added")
    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    @log_decorator("Book removed")
    def remove_book(self, title):
        original_length = len(self.books)
        self.books = [book for book in self.books if book.title != title]
        if len(self.books) == original_length:
            raise ValueError("Book not found")
        self.save_books()


    @log_decorator("Displayed all books")
    def display_all_books(self):
        return self.books

    @log_decorator("Displayed available books")
    def display_available_books(self):
        return [book for book in self.books if not book.is_loaned]

    @log_decorator("Displayed borrowed books")
    def display_borrowed_books(self):
        return [book for book in self.books if book.is_loaned]

    @log_decorator("Displayed books by category")
    def display_books_by_category(self, category):
        return [book for book in self.books if book.genre.lower() == category.lower()]

    @log_decorator("Book borrowed")
    def borrow_book(self, title):
        for book in self.books:
            if book.title == title and not book.is_loaned:
                book.is_loaned = True
                self.save_books()
                return
        raise ValueError("Book not available")

    @log_decorator("Book returned")
    def return_book(self, title):
        for book in self.books:
            if book.title == title and book.is_loaned:
                book.is_loaned = False
                self.save_books()
                return
        raise ValueError("Book not borrowed")
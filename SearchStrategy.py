# --- Design Patterns ---
# Strategy Pattern for Search
from abc import ABC, abstractmethod
from typing import List
from Book import Book

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, books: List[Book], query: str) -> List[Book]:
        pass

class SearchByTitle(SearchStrategy):
    def search(self, books: List[Book], query: str) -> List[Book]:
        return [book for book in books if query.lower() in book.title.lower()]

class SearchByAuthor(SearchStrategy):
    def search(self, books: List[Book], query: str) -> List[Book]:
        return [book for book in books if query.lower() in book.author.lower()]

class SearchByCategory(SearchStrategy):
    def search(self, books: List[Book], query: str) -> List[Book]:
        return [book for book in books if query.lower() in book.genre.lower()]

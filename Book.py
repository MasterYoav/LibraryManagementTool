# --- Book Management ---
class Book:
    def __init__(self, title: str, author: str, is_loaned: bool, copies: int, genre: str, year: int):
        self.title = title
        self.author = author
        self.is_loaned = is_loaned
        self.copies = copies
        self.genre = genre
        self.year = year

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "is_loaned": "Yes" if self.is_loaned else "No",
            "copies": self.copies,
            "genre": self.genre,
            "year": self.year
        }

    def get_copies(self):
        return self.copies


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Library import Library
from UserManager import UserManager
from BookFactory import BookFactory
from SearchStrategy import SearchByTitle, SearchByAuthor, SearchByCategory
from log_decorator import log_decorator



class LibraryGUI:
    def __init__(self):
        # Clear log file at the start of the program
        with open("log.txt", "w", encoding="utf-8") as log_file:
            log_file.write("")  # Wipe all previous logs

        self.library = Library()
        self.user_manager = UserManager()
        self.current_user = None
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.create_login_register_menu()
        self.root.mainloop()

    def create_login_register_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Welcome to the Library", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Login", command=self.login, width=20).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register, width=20).pack(pady=5)

    def create_main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Library Main Menu", font=("Arial", 16)).pack(pady=10)

        # Load and display the image
        try:
            self.image = tk.PhotoImage(file="images/books_image.png")
            image_label = tk.Label(self.root, image=self.image)
            image_label.pack(side=tk.LEFT, padx=20, pady=20)  # Place the image on the left side
        except Exception as e:
            print(f"Error loading image: {e}")

        options = [
            ("Add Book", self.add_book),
            ("Remove Book", self.remove_book),
            ("Search Book", self.search_book),
            ("View Books", self.view_books),
            ("Lend Book", self.lend_book),
            ("Return Book", self.return_book),
            ("Popular Books", self.popular_books)
        ]

        for text, command in options:
            tk.Button(self.root, text=text, command=command, width=20).pack(pady=5)

        tk.Button(self.root, text="Logout", command=self.logout, width=20).pack(pady=5)

    def create_scrollable_frame(self, title, callback):
        self.clear_window()

        tk.Label(self.root, text=title, font=("Arial", 16)).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Button(self.root, text="Back", command=callback, width=20).pack(pady=10)

        return scrollable_frame

    def login(self):
        self.clear_window()

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        username_label = tk.Label(self.root, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        password_label = tk.Label(self.root, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        @log_decorator("Login attempted")
        def perform_login():
            username = username_entry.get()
            password = password_entry.get()
            if self.user_manager.authenticate_user(username, password):
                self.current_user = username
                messagebox.showinfo("Success", "Login Successful")
                self.create_main_menu()
            else:
                messagebox.showerror("Error", "Invalid username or password")

        tk.Button(self.root, text="Login", command=perform_login, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_login_register_menu, width=20).pack(pady=10)

    def register(self):
        self.clear_window()


        tk.Label(self.root, text="Register", font=("Arial", 16)).pack(pady=10)

        username_label = tk.Label(self.root, text="Username:")
        username_label.pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        password_label = tk.Label(self.root, text="Password:")
        password_label.pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        @log_decorator("Registration attempted")
        def perform_register():
            username = username_entry.get()
            password = password_entry.get()
            try:
                self.user_manager.register_user(username, password)
                messagebox.showinfo("Success", "Registration Successful")
                self.create_login_register_menu()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Register", command=perform_register, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_login_register_menu, width=20).pack(pady=10)

    def add_book(self):
        self.clear_window()

        tk.Label(self.root, text="Add Book", font=("Arial", 16)).pack(pady=10)

        # Entry fields for book details
        fields = ["Title", "Author", "Year", "Genre", "Copies", "Is Loaned (Yes/No)"]
        entries = {}
        for field in fields:
            tk.Label(self.root, text=f"{field}:").pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry

        def perform_add():
            try:
                # Parse the is_loaned field as a boolean
                is_loaned = entries["Is Loaned (Yes/No)"].get().strip().lower() == "yes"

                book = BookFactory.create_book(
                    title=entries["Title"].get(),
                    author=entries["Author"].get(),
                    is_loaned=is_loaned,
                    copies=int(entries["Copies"].get()),
                    genre=entries["Genre"].get(),
                    year=int(entries["Year"].get())
                )
                self.library.add_book(book)
                messagebox.showinfo("Success", "Book added successfully")
                self.create_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please check the fields.")

        tk.Button(self.root, text="Add Book", command=perform_add, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, width=20).pack(pady=10)

    def remove_book(self):
        self.clear_window()

        tk.Label(self.root, text="Remove Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Title:").pack()
        title_entry = tk.Entry(self.root)
        title_entry.pack()

        def perform_remove():
            title = title_entry.get()
            self.library.remove_book(title)
            messagebox.showinfo("Success", "Book removed successfully")
            self.create_main_menu()

        tk.Button(self.root, text="Remove Book", command=perform_remove, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, width=20).pack(pady=10)

    def search_book(self):
        self.clear_window()

        tk.Label(self.root, text="Search Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Search By:").pack()
        search_var = tk.StringVar(value="Title")

        # Search options
        options = [("Title", "Title"), ("Author", "Author"), ("Genre", "Genre")]
        for text, value in options:
            tk.Radiobutton(self.root, text=text, variable=search_var, value=value).pack()

        tk.Label(self.root, text="Search Query:").pack()
        query_entry = tk.Entry(self.root)
        query_entry.pack()

        def perform_search():
            query = query_entry.get()
            strategy = None
            if search_var.get() == "Title":
                strategy = SearchByTitle()
            elif search_var.get() == "Author":
                strategy = SearchByAuthor()
            elif search_var.get() == "Genre":
                strategy = SearchByCategory()

            if strategy:
                results = strategy.search(self.library.books, query)
                if results:
                    result_frame = self.create_scrollable_frame("Search Results", self.search_book)
                    for book in results:
                        tk.Label(result_frame,
                                 text=f"{book.title} by {book.author} ({book.year}) - {book.copies} copies").pack()
                else:
                    messagebox.showinfo("No Results", "No books found for your query.")

        tk.Button(self.root, text="Search", command=perform_search, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, width=20).pack(pady=10)

    def view_books(self):
        scrollable_frame = self.create_scrollable_frame("View Books", self.create_main_menu) # Add a scroll wheel

        books = self.library.books
        for book in books:
            tk.Label(scrollable_frame,
                     text=f"{book.title} by {book.author} ({book.year}) - {book.copies} copies",
                     anchor="center", # Aligns text in the center
                     justify="center", # Centers multi-line text
                     width=80,  # Adjust width to ensure proper centering
                     ).pack(fill=tk.X, pady=2) # Expands label to fit width

    def lend_book(self):
        self.clear_window()

        tk.Label(self.root, text="Lend Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Title:").pack()
        title_entry = tk.Entry(self.root)
        title_entry.pack()

        def perform_lend():
            title = title_entry.get()
            if self.library.borrow_book(title):
                messagebox.showinfo("Success", "Book borrowed successfully")
            else:
                messagebox.showerror("Error", "Book not available")

        tk.Button(self.root, text="Lend Book", command=perform_lend, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, width=20).pack(pady=10)

    def return_book(self):
        self.clear_window()

        tk.Label(self.root, text="Return Book", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Title:").pack()
        title_entry = tk.Entry(self.root)
        title_entry.pack()

        def perform_return():
            title = title_entry.get()
            self.library.return_book(title)
            messagebox.showinfo("Success", "Book returned successfully")

        tk.Button(self.root, text="Return Book", command=perform_return, width=20).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_main_menu, width=20).pack(pady=10)

    @log_decorator("Displayed popular books")
    def popular_books(self):
        scrollable_frame = self.create_scrollable_frame("Popular Books", self.create_main_menu)

        books = sorted(self.library.books, key=lambda b: -b.get_copies())[:5]
        for book in books:
            tk.Label(scrollable_frame,
                          text=f"{book.title} by {book.author} ({book.year}) - {book.copies} copies",
                          anchor="center",  # Aligns text in the center
                          justify="center",  # Centers multi-line text
                          width=80,  # Adjust width to ensure proper centering
                          ).pack(fill=tk.X, pady=2)  # Expands label to fit width

    def logout(self):
        self.current_user = None
        self.create_login_register_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    LibraryGUI()
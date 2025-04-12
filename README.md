# LibraryManagementTool

A Python-based command-line application for managing books, members, and loans in a small library.  
This project was developed as part of an Object-Oriented Programming (OOP) course, showcasing practical design using classes, files, and interaction menus.

---

## 📚 Features

- **Book Management**: Add, update, delete, and view books
- **Member Management**: Register, view, and manage library members
- **Loan System**: Lend books, return books, and check due dates
- **Data Persistence**: All data is stored in local JSON files
- **Modular OOP Design**: Code is structured using Python classes and clean logic

---

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/MasterYoav/LibraryManagementTool.git
cd LibraryManagementTool
```

2. Run the program:

```bash
python main.py
```

> Make sure you have Python 3.x installed

---

## 🚀 Usage

Upon launching the script, the program provides an interactive menu.  
You can choose to:

- Add/View/Delete Books
- Register/View Members
- Lend and return books
- View book availability and due dates

All data is saved inside the `data/` directory using `.json` format.

---

## 🧱 Project Structure

```plaintext
LibraryManagementTool/
├── main.py               # Main menu and logic control
├── book.py               # Book class and methods
├── member.py             # Member class and methods
├── loan.py               # Loan tracking logic
├── utils/
│   └── file_handler.py   # JSON file loading/saving helpers
├── data/
│   ├── books.json
│   ├── members.json
│   └── loans.json
└── README.md             # This file
```

---

## 📄 License

This project is licensed under the MIT License.  

---

## 👨‍🎓 Author

Developed by **Yoav Peretz**  
B.Sc. Computer Science  
Course: Object-Oriented Programming (OOP)

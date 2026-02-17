# Library Management System

A comprehensive Python-based library management system that allows users to manage books, members, and borrowing operations in a library.

## Project Overview

This project implements a complete library management system with the following core features:
- Book inventory management
- Member registration and management
- Book borrowing and return operations
- Book search functionality
- Availability tracking
- Genre-based book filtering and statistics

## Project Structure

```
Library_Management_System/
├── book.py                  # Book class definition
├── member.py                # Member class definition
├── library.py               # Library class definition
├── main.py                  # Main application and demonstrations
├── test_library.py          # Comprehensive unit test suite (47 tests)
├── README.md                # Project documentation
├── EXECUTION_OUTPUT.txt     # Captured output from main.py and test execution
├── TECHNICAL_NOTES.txt      # Architecture and implementation details
├── ERROR_HANDLING.txt       # Error handling strategy documentation
├── LOGGING_SETUP.txt        # Logging configuration details
├── TEST_SUMMARY.txt         # Detailed test descriptions
└── PROJECT_INDEX.txt        # Master project reference
```

## Classes

### Book (`book.py`)

Represents a book in the library with the following attributes and methods:

**Attributes:**
- `book_id` (int): Unique identifier for the book
- `title` (str): Title of the book
- `author` (str): Author of the book
- `genre` (str): Genre/category of the book
- `is_available` (bool): Availability status (True if available, False if borrowed)
- `borrowed_at` (datetime): Timestamp when the book was borrowed (None if available)
- `borrowed_by` (Member): Reference to member who borrowed the book (None if available)
- `returned_at` (datetime): Timestamp when the book was last returned (None if never returned)
- `returned_by` (Member): Reference to member who returned the book (None if never returned)

**Methods:**
- `__init__(book_id, title, author, genre)`: Initializes a Book with ID, title, author, and genre; marks it as available by default; initializes temporal tracking fields
- `borrow(member=None)`: Marks the book as borrowed if available and records timestamp and member who borrowed it
- `return_book(member=None)`: Marks the book as available when returned and records timestamp and member who returned it
- `get_borrow_details()`: Returns dictionary with borrowed_at timestamp, borrowed_by member name, and borrowed_by_id; None if book is available
- `get_return_details()`: Returns dictionary with returned_at timestamp, returned_by member name, and returned_by_id; None if book is currently borrowed
- `__str__()`: Returns a string representation of the book with its title, author, ID, and availability status

### Member (`member.py`)

Represents a library member with the following attributes and methods:

**Attributes:**
- `member_id` (int): Unique identifier for the member
- `name` (str): Member's full name
- `age` (int): Member's age
- `contact_info` (str): Member's contact information (email/phone)
- `borrowed_books` (list): List of books currently borrowed by the member

**Methods:**; passes member context for temporal tracking
- `return_book(book)`: Removes a book from the member's borrowed list and marks it as available; passes member context for temporal trackingn empty borrowed books list
- `borrow_book(book)`: Allows a member to borrow a book if they haven't reached the 5-book limit and the book is available
- `return_book(book)`: Removes a book from the member's borrowed list and marks it as available in the library
- `__str__()`: Returns a string representation of the member including their name, ID, and list of borrowed books

### Library (`library.py`)

Manages all books, members, and operations in the library with the following methods:

**Attributes:**
- `books` (list): List of all books in the library
- `members` (list): List of all registered members

**Methods:**
- `__init__()`: Initializes the Library with empty lists for books and members
- `add_book(book)`: Adds a single book to the library's collection
- `add_books(*books)`: Adds multiple books to the library at once using variable arguments
- `remove_book(book)`: Removes a specific book from the library if it exists
- `add_member(member)`: Adds a single member to the library's member list
- `add_members(*members)`: Adds multiple members to the library at once using variable arguments
- `remove_member(member)`: Removes a specific member from the library's member list if they exist
- `display_books()`: Displays all books currently in the library's collection
- `display_members()`: Displays all registered members in the library
- `issue_book(book, member)`: Issues a book to a member if available; passes member context for temporal tracking
- `return_book(book, member)`: Processes book return from member; passes member context for temporal tracking
- `available_books(genre=None)`: Returns a list of available books, optionally filtered by genre
- `members_with_borrowed_books(members)`: Returns a list of members who have borrowed books from the library
- `search_book(keyword)`: Searches for a book by title or author using a keyword (case-insensitive); returns the first match or None
- `most_popular_genre_from_issued_books()`: Determines the most popular genre among currently issued (borrowed) books
- `get_book_borrow_details(book)`: Returns dictionary with current borrow timestamp and member info if book is borrowed; None if available
- `get_book_return_details(book)`: Returns dictionary with last return timestamp and member info if book has been returned; None if never returned
- `get_book_history(book)`: Returns complete history dictionary including book ID, title, current status, borrow details, and return details

## Main Application (`main.py`)

The main module provides a demonstration of the library management system with the following functions:

- `create_sample_data_and_operations(library)`: Creates sample books and members, adds them to the library, issues books to members, and demonstrates return operations
- `display_available_books(library)`: Displays all books currently available for borrowing in the library
- `display_available_books_by_genre(library, genre)`: Displays all available books of a specific genre
- `search_books_by_keyword(library, keyword)`: Searches for books by keyword and displays matching results based on title or author
- `display_members_with_borrowed_books(library)`: Displays all members who have currently borrowed books from the library
- `display_books_count_by_genre(library)`: Displays the total count of books in the library grouped by genre
- `display_books_count_by_genre_by_issuance(library)`: Displays the count of currently issued (borrowed) books grouped by genre
- `display_most_popular_genre_from_issued_books(library)`: Displays the most popular genre among all currently issued books
- `main()`: Main entry point that orchestrates the entire library management system demonstration

## Documentation Files

### EXECUTION_OUTPUT.txt
Contains captured output from both the main application and test suite execution:
- **Main Application Output**: Complete demonstration showing all 21 books, 7 members, borrowing operations, returns, searches, and analytics
- **Test Suite Output**: All 47 unit tests passing with execution time of 0.005 seconds
- **Execution Summary**: Performance metrics, capabilities demonstrated, and error handling examples
- **Purpose**: Provides proof of successful system execution and demonstrates all features in action

### Other Documentation Files
- **TECHNICAL_NOTES.txt**: Architecture overview, design patterns, implementation details, complexity analysis
- **ERROR_HANDLING.txt**: Strategy for error handling with 11 try-except blocks and validation examples
- **LOGGING_SETUP.txt**: Logging configuration with file and console handlers, log level settings
- **TEST_SUMMARY.txt**: Detailed descriptions of all 47 unit tests across 4 test classes
- **PROJECT_INDEX.txt**: Master reference document for the entire project

## Features

1. **Book Management**: Add, remove, and search for books
2. **Member Management**: Register and manage library members
3. **Borrowing System**: Members can borrow up to 5 books at a time
4. **Book Return**: Track book returns and update availability
5. **Availability Tracking**: Monitor which books are available or borrowed
9. **Datetime Tracking**: Capture when books are borrowed/returned and by which member
10. **Borrowing History**: Query complete borrowing history including timestamps and member associations
11. **Audit Trail**: Comprehensive temporal tracking for operational intelligence and auditing
6. **Genre Filtering**: Filter books by genre and view statistics
7. **Search Functionality**: Find books by title or author name
8. **Popular Genre Analysis**: Identify the most popular genre among borrowed books

## Usage

To run the library management system:

```bash
python main.py
```

This will execute the main demonstration which includes:
- Creating 21 sample books across multiple genres
- Creating 7 sample members
- Issuing books to members
- Returning books
- Displaying available books
- Filtering books by genre
- Searching for books by keyword
- Displaying member information and book statistics

## Constraints

- Each member can borrow a maximum of 5 books at a time
- A book can only be borrowed if it is currently available
- A member cannot return a book they did not borrow

## Example Output

The system displays formatted information about:
- All books in the library with availability status
- All registered members
- Available books (all or filtered by genre)
- Members with borrowed books
- Book counts by genre
- Most popular genres among borrowed books
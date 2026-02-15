import logging
from matplotlib.style import library
from library import Library
from book import Book
from member import Member

# Configure logging to log messages to both a file and the console with appropriate formatting and error handling
try:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('library_management.log'),
            logging.StreamHandler()
        ]
    )
except IOError as e:
    print(f"Error configuring logging: {str(e)}")
    raise
except Exception as e:
    print(f"Unexpected error during logging configuration: {str(e)}")
    raise

logger = logging.getLogger(__name__)

# Creates sample books and members, adds them to the library, issues books to members, and demonstrates return operations
def create_sample_data_and_operations(library):

    # Create books and add them to the library, then display the books
    book1 = Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "Fiction")
    book2 = Book(2, "To Kill a Mockingbird", "Harper Lee", "Fiction")
    book3 = Book(3, "The Catcher in the Rye", "J.D. Salinger", "Fiction")
    book4 = Book(4, "War and Peace", "Leo Tolstoy", "Fiction")
    book5 = Book(5, "Pride and Prejudice", "Jane Austen", "Fiction")
    book6 = Book(6, "The Fault in Our Stars", "John Green", "Fiction")
    book7 = Book(7, "Brave New World", "Aldous Huxley", "Dystopian")
    book8 = Book(8, "Fahrenheit 451", "Ray Bradbury", "Dystopian")
    book9 = Book(9, "The Hunger Games", "Suzanne Collins", "Dystopian")
    book10 = Book(10, "The Handmaid's Tale", "Margaret Atwood", "Dystopian")
    book11 = Book(11, "The Road", "Cormac McCarthy", "Dystopian")
    book12 = Book(12, "The Hobbit", "J.R.R. Tolkien", "Fantasy")
    book13 = Book(13, "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy")
    book14 = Book(14, "The Chronicles of Narnia", "C.S. Lewis", "Fantasy")
    book15 = Book(15, "Moby Dick", "Herman Melville", "Adventure")
    book16 = Book(16, "The Alchemist", "Paulo Coelho", "Adventure")
    book17 = Book(17, "The Odyssey", "Homer", "Adventure")
    book18 = Book(18, "The Da Vinci Code", "Dan Brown", "Thriller")
    book19 = Book(19, "The Shining", "Stephen King", "Thriller")
    book20 = Book(20, "The Girl with the Dragon Tattoo", "Stieg Larsson", "Mystery")
    book21 = Book(21, "Art in 1984", "George Orwell", "Literature")
    library.add_books(book1, book2, book3, book4, book5, book6, book7, book8, book9, book10, book11, book12, book13, book14, book15, book16, book17, book18, book19, book20, book21)
    library.display_books()
    
    # Create members, add them to the library and display members
    member1 = Member(1, "Alice", 30, "alice@example.com")
    member2 = Member(2, "Bob", 25, "bob@example.com")
    member3 = Member(3, "Charlie", 35, "charlie@example.com")
    member4 = Member(4, "David", 28, "david@example.com")
    member5 = Member(5, "Eve", 22, "eve@example.com")
    member6 = Member(6, "Frank", 40, "frank@example.com")
    member7 = Member(7, "Grace", 27, "grace@example.com")
    library.add_members(member1, member2, member3, member4, member5, member6, member7)
    library.display_members()

    # Issue books to members and display the updated member information
    logger.info("\n================== Issuing Books ==================")
    library.issue_book(book1, member1)
    library.issue_book(book2, member1)
    library.issue_book(book3, member2)
    library.issue_book(book4, member3)
    library.issue_book(book5, member4)
    library.issue_book(book6, member5)
    library.issue_book(book7, member6)
    library.issue_book(book8, member6)
    library.issue_book(book9, member1)
    library.issue_book(book10, member2)
    library.issue_book(book20, member3)
    library.issue_book(book21, member5)

    # Attempt to issue a book that is already borrowed
    library.issue_book(book1, member4)
    library.issue_book(book3, member1)

    # Return books from members
    logger.info("\n================== Returning Books ==================")
    library.return_book(book1, member1)
    library.return_book(book3, member2)
    library.return_book(book5, member4)
    library.return_book(book10, member2)

    # Attempt to return a book that was not borrowed by the member
    library.return_book(book11, member7)
    library.return_book(book15, member2)

# Displays all books currently issued (borrowed) in the library
def display_issued_books(library):
    print("\n================== Books currently issued (borrowed) in the library ===================")
    issued_books = library.issued_books()
    if issued_books:
        for book in issued_books:
            print(book)
    else:
        print("No books are currently issued (borrowed).")

# Displays all books currently available for borrowing in the library
def display_available_books(library):
    print("\n================== Books currently available in the library ==================")
    available_books = library.available_books()
    if available_books:
        for book in available_books:
            print(book)
    else:
        print("No books are currently available.")

# Displays all available books of a specific genre
def display_available_books_by_genre(library, genre):
    print(f"\n================== Books currently available in the library of genre - {genre} ==================")
    available_books = library.available_books(genre=genre)
    if available_books:
        for book in available_books:
            print(book)
    else:
        print(f"No books of genre {genre} are currently available.")

# Searches for books by keyword and displays matching results based on title or author
def search_books_by_keyword(library, keyword):
    print(f"\n================== Search for a book by keyword '{keyword}' ==================")
    matching_books = library.search_books(keyword=keyword)
    if matching_books:
        for book in matching_books:
            print(book) 
    else:
        print(f"No books found with keyword '{keyword}'.")

# Displays all members who have currently borrowed books from the library
def display_members_with_borrowed_books(library):
    print("\n================== Members with borrowed books ==================")
    members_with_borrowed_books = library.members_with_borrowed_books(library.members)
    if members_with_borrowed_books:
        for member in members_with_borrowed_books:
            print(member)
    else:
        print("No members have borrowed books from the library.")

# Displays the total count of books in the library grouped by genre
def display_books_count_by_genre(library):
    print("\n================== Books count by genre ==================")
    genre_counts = library.books_count_by_genre()
    if genre_counts:
        for genre, count in genre_counts.items():
            print(f"{genre}: {count}")
    else:
        print("No books in the library to count by genre.")

# Displays the count of currently issued (borrowed) books grouped by genre
def display_books_count_by_genre_by_issuance(library):
    print("\n================== Issued Books count by genre ==================")
    genre_counts = library.books_count_by_genre(check_for_issuance=True)
    if genre_counts:
        for genre, count in genre_counts.items():
            print(f"{genre}: {count}")
    else:
        print("No books in the library to count by genre.")

# Displays the most popular genre among all currently issued books
def display_most_popular_genre_from_issued_books(library):
    print("\n================== Most popular genre amongst issued books ==================")
    most_popular_genres = library.most_popular_genre_from_issued_books()
    if most_popular_genres:
        for genre in most_popular_genres:
            print(genre)
    else:
        print("No issued books to determine most popular genre.\n")

# Main entry point that orchestrates the entire library management system demonstration
def main():
    try:
        # Create library instance
        library = Library()
        logger.info("Library Management System started")
        
        create_sample_data_and_operations(library)

        # Display members with borrowed books
        display_members_with_borrowed_books(library)

        # Display issued and available books
        display_issued_books(library)
        display_available_books(library)

        # Display available books by genre
        display_available_books_by_genre(library, genre="Fiction")
        display_available_books_by_genre(library, genre="Dystopian")

        # Search for books by keyword in title or author
        search_books_by_keyword(library, keyword="the")
        search_books_by_keyword(library, keyword="tolkien")
        search_books_by_keyword(library, keyword="kill")
        
        # Display count of books by genre
        display_books_count_by_genre(library)

        # Display count of issued books by genre
        display_books_count_by_genre_by_issuance(library)

        # Display the most popular genre among issued books
        display_most_popular_genre_from_issued_books(library)
        
        logger.info("Library Management System completed successfully")
    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
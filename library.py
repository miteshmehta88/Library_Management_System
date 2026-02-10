from member import Member
from book import Book

class Library:
    # Initializes the Library with empty lists for books and members
    def __init__(self):
        self.books = []
        self.members = []

    # Adds a single book to the library's collection
    def add_book(self, book):
        self.books.append(book)

    # Adds multiple books to the library at once using variable arguments
    def add_books(self, *books):
        self.books.extend(books)

    # Removes a specific book from the library if it exists
    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)

    # Adds a single member to the library's member list
    def add_member(self, member):
        self.members.append(member)
    
    # Adds multiple members to the library at once using variable arguments
    def add_members(self, *members):
        self.members.extend(members)

    # Removes a specific member from the library's member list if they exist
    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)

    # Displays all books currently in the library's collection
    def display_books(self):
        print("\n================== Books in the Library ==================")
        for book in self.books:
            print(book)

    # Displays all registered members in the library
    def display_members(self):
        print("\n==================== Library Members ====================")
        for member in self.members:
            print(member)

    # Issues a book to a member if the book is available; otherwise prints an error message
    def issue_book(self, book, member):
        if book in self.books and book.is_available:
            member.borrow_book(book)
        else:
            print(f"{book.title} is not available for borrowing.")

    # Processes the return of a book from a member; validates that the member actually borrowed it
    def return_book(self, book, member):
        if book in member.borrowed_books:
            member.return_book(book)
        else:
            print(f"{member.name} cannot return {book.title}. Book not borrowed by this member.")  

    # Returns a list of available books, optionally filtered by genre
    def available_books(self, genre=None):
        if genre:
            return [book for book in self.books if book.is_available and book.genre == genre]
        return [book for book in self.books if book.is_available] 
    
    def issued_books(self, genre=None):
        if genre:
            return [book for book in self.books if not book.is_available and book.genre == genre]
        return [book for book in self.books if not book.is_available]
    
    # Returns a list of members who have borrowed books from the library
    def members_with_borrowed_books(self, members):
        return [member for member in members if member.borrowed_books]
    
    # Searches for a book by title or author using a keyword (case-insensitive); returns the first match or None
    def search_books(self, keyword):
        matches = []
        keyword = keyword.lower()
        for book in self.books:
            if keyword in book.title.lower() or keyword in book.author.lower():
                matches.append(book)
        return matches

    # Determines the count of books in the library grouped by genre; can optionally count only available books
    def books_count_by_genre(self, check_for_issuance=False):
        count_by_genre = {}
        for book in self.books:
            if not check_for_issuance or (check_for_issuance and not book.is_available):
                genre = book.genre
                count_by_genre[genre] = count_by_genre.get(genre, 0) + 1
        return count_by_genre

    # Determines the most popular genre among currently issued (borrowed) books
    def most_popular_genre_from_issued_books(self):
        count_by_genre = self.books_count_by_genre(check_for_issuance=True)
        max_count = max(count_by_genre.values()) if count_by_genre else 0
        return [genre for genre, count in count_by_genre.items() if count == max_count]
    



from book import Book

class Member:
    # Initializes a Member with ID, name, age, contact info, and an empty borrowed books list
    def __init__(self, member_id, name, age, contact_info):
        self.member_id = member_id
        self.name = name
        self.age = age
        self.contact_info = contact_info
        self.borrowed_books = []

    # Allows a member to borrow a book if they haven't reached the 5-book limit and the book is available
    def borrow_book(self, book):
        if len(self.borrowed_books) < 5 and book.is_available_to_borrow():
            self.borrowed_books.append(book)
            book.borrow()
            print(f"{self.name} has borrowed {book.title}.")
        else:
            print(f"{self.name} cannot borrow {book.title}. Maximum limit reached or book not available.")
            
    # Removes a book from the member's borrowed list and marks it as available in the library
    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.return_book()
            print(f"{self.name} has returned {book.title}.")
        else:
            print(f"{self.name} cannot return {book.title}. Book not borrowed by this member.")

    # Returns a string representation of the member including their name, ID, and list of borrowed books
    def __str__(self):        
        return f"{self.name} (ID: {self.member_id}) - Borrowed Books: {[book.title for book in self.borrowed_books]}" 

class Book:
    # Initializes a Book with ID, title, author, and genre; marks it as available by default
    def __init__(self, book_id, title, author, genre):  
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre 
        self.is_available = True

    # Marks the book as borrowed if it's available; returns True if successful, False otherwise
    def borrow(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    # Marks the book as available when it is returned to the library
    def return_book(self):
        self.is_available = True

    # Returns the availability status of the book
    def is_available_to_borrow(self):
        return self.is_available
    
    # Returns a string representation of the book with its title, author, ID, and availability status
    def __str__(self):
        return f"{self.title} by {self.author} (ID: {self.book_id}) - {'Available' if self.is_available else 'Not Available'}"

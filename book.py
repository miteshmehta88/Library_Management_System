from datetime import datetime

class Book:
    # Initializes a Book with ID, title, author, and genre; marks it as available by default
    # Also initializes datetime tracking fields for borrowing and returning
    def __init__(self, book_id, title, author, genre):  
        try:
            if not isinstance(book_id, int) or book_id <= 0:
                raise ValueError("book_id must be a positive integer")
            if not isinstance(title, str) or not title.strip():
                raise ValueError("title must be a non-empty string")
            if not isinstance(author, str) or not author.strip():
                raise ValueError("author must be a non-empty string")
            if not isinstance(genre, str) or not genre.strip():
                raise ValueError("genre must be a non-empty string")
            
            self.book_id = book_id
            self.title = title
            self.author = author
            self.genre = genre 
            self.is_available = True
            # Datetime tracking fields for borrowing and returning history
            self.borrowed_at = None  # Timestamp when book was borrowed
            self.borrowed_by = None  # Member object who borrowed the book
            self.returned_at = None  # Timestamp when book was last returned
            self.returned_by = None  # Member object who returned the book
        except ValueError as e:
            raise ValueError(f"Error creating Book: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error creating Book: {str(e)}")

    # Marks the book as borrowed with timestamp and member information
    # Records when the book was borrowed and by which member
    def borrow(self, member=None):
        if self.is_available:
            self.is_available = False
            self.borrowed_at = datetime.now()
            self.borrowed_by = member
            return True
        return False

    # Marks the book as available with timestamp and member information who returned it
    # Records when the book was returned and by which member
    def return_book(self, member=None):
        self.is_available = True
        self.returned_at = datetime.now()
        self.returned_by = member

    # Returns the availability status of the book
    def is_available_to_borrow(self):
        return self.is_available
    
    # Returns borrowing details if book is currently borrowed (not available)
    # Returns tuple: (borrowed_time, member_name) or None if book is available
    def get_borrow_details(self):
        if not self.is_available and self.borrowed_at and self.borrowed_by:
            member_name = self.borrowed_by.name if hasattr(self.borrowed_by, 'name') else str(self.borrowed_by)
            return {
                'borrowed_at': self.borrowed_at.strftime('%Y-%m-%d %H:%M:%S'),
                'borrowed_by': member_name,
                'borrowed_by_id': self.borrowed_by.member_id if hasattr(self.borrowed_by, 'member_id') else None
            }
        return None
    
    # Returns last return details if book was previously borrowed and returned
    # Returns tuple: (return_time, member_name) or None if no return history
    def get_return_details(self):
        if self.is_available and self.returned_at and self.returned_by:
            member_name = self.returned_by.name if hasattr(self.returned_by, 'name') else str(self.returned_by)
            return {
                'returned_at': self.returned_at.strftime('%Y-%m-%d %H:%M:%S'),
                'returned_by': member_name,
                'returned_by_id': self.returned_by.member_id if hasattr(self.returned_by, 'member_id') else None
            }
        return None    
    # Returns a string representation of the book with its title, author, ID, and availability status
    def __str__(self):
        return f"{self.title} by {self.author} (ID: {self.book_id}) - {'Available' if self.is_available else 'Not Available'}"
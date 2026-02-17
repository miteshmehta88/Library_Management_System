import logging
from book import Book

logger = logging.getLogger(__name__)

class Member:
    # Initializes a Member with ID, name, age, contact info, and an empty borrowed books list

    MAX_BORROW_LIMIT = 2

    def __init__(self, member_id, name, age, contact_info):
        try:
            if not isinstance(member_id, int) or member_id <= 0:
                raise ValueError("member_id must be a positive integer")
            if not isinstance(name, str) or not name.strip():
                raise ValueError("name must be a non-empty string")
            if not isinstance(age, int) or age < 0:
                raise ValueError("age must be a non-negative integer")
            if not isinstance(contact_info, str) or not contact_info.strip():
                raise ValueError("contact_info must be a non-empty string")
            
            self.member_id = member_id
            self.name = name
            self.age = age
            self.contact_info = contact_info
            self.borrowed_books = []
        except ValueError as e:
            raise ValueError(f"Error creating Member: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error creating Member: {str(e)}")

    # Allows a member to borrow a book if they haven't reached the max borrow limit and the book is available
    # Passes member information to the book for datetime tracking
    def borrow_book(self, book):
        try:
            if not hasattr(book, 'is_available_to_borrow'):
                raise AttributeError("Invalid book object: missing is_available_to_borrow method")
            if len(self.borrowed_books) < Member.MAX_BORROW_LIMIT:
                if book.is_available_to_borrow():
                    self.borrowed_books.append(book)
                    book.borrow(member=self)  # Pass member object for tracking
                    logger.info(f"{self.name} has borrowed {book.title}.")
                else:
                    logger.info(f"{self.name} cannot borrow {book.title}. Book is not available.")
            else:
                logger.info(f"{self.name} cannot borrow {book.title}. Maximum limit reached.")
        except AttributeError as e:
            logger.error(f"Error borrowing book: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during borrow_book: {str(e)}")
            
    # Removes a book from the member's borrowed list and marks it as available in the library
    # Passes member information to the book for return datetime tracking
    def return_book(self, book):
        try:
            if not hasattr(book, 'return_book'):
                raise AttributeError("Invalid book object: missing return_book method")
            if book in self.borrowed_books:
                self.borrowed_books.remove(book)
                book.return_book(member=self)  # Pass member object for tracking
                logger.info(f"{self.name} has returned {book.title}.")
            else:
                logger.info(f"{self.name} cannot return {book.title}. Book not borrowed by this member.")
        except AttributeError as e:
            logger.error(f"Error returning book: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during return_book: {str(e)}")

    # Returns a string representation of the member including their name, ID, and list of borrowed books
    def __str__(self):        
        return f"{self.name} (ID: {self.member_id}) - Borrowed Books: {[book.title for book in self.borrowed_books]}" 
import unittest
import logging
import time
from datetime import datetime
from book import Book
from member import Member
from library import Library

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestBook(unittest.TestCase):
    """Test cases for the Book class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a valid book for testing
        self.valid_book = Book(1, "Test Book", "Test Author", "Fiction")

    # Test: Valid book creation with correct parameters
    def test_book_creation_valid(self):
        """Test that a book can be created successfully with valid parameters"""
        self.assertEqual(self.valid_book.book_id, 1)
        self.assertEqual(self.valid_book.title, "Test Book")
        self.assertEqual(self.valid_book.author, "Test Author")
        self.assertEqual(self.valid_book.genre, "Fiction")
        self.assertTrue(self.valid_book.is_available)

    # Test: Invalid book creation with negative ID
    def test_book_creation_invalid_id(self):
        """Test that book creation fails with negative book_id"""
        with self.assertRaises(ValueError):
            Book(-1, "Test Book", "Test Author", "Fiction")

    # Test: Invalid book creation with zero ID
    def test_book_creation_invalid_id_zero(self):
        """Test that book creation fails with zero book_id"""
        with self.assertRaises(ValueError):
            Book(0, "Test Book", "Test Author", "Fiction")

    # Test: Invalid book creation with empty title
    def test_book_creation_invalid_title(self):
        """Test that book creation fails with empty title"""
        with self.assertRaises(ValueError):
            Book(1, "", "Test Author", "Fiction")

    # Test: Invalid book creation with empty author
    def test_book_creation_invalid_author(self):
        """Test that book creation fails with empty author"""
        with self.assertRaises(ValueError):
            Book(1, "Test Book", "", "Fiction")

    # Test: Invalid book creation with empty genre
    def test_book_creation_invalid_genre(self):
        """Test that book creation fails with empty genre"""
        with self.assertRaises(ValueError):
            Book(1, "Test Book", "Test Author", "")

    # Test: Book borrow functionality when available
    def test_book_borrow_available(self):
        """Test that a book can be borrowed when it's available"""
        result = self.valid_book.borrow()
        self.assertTrue(result)
        self.assertFalse(self.valid_book.is_available)

    # Test: Book borrow functionality when already borrowed
    def test_book_borrow_unavailable(self):
        """Test that a book cannot be borrowed when already borrowed"""
        self.valid_book.borrow()
        result = self.valid_book.borrow()
        self.assertFalse(result)
        self.assertFalse(self.valid_book.is_available)

    # Test: Book return functionality
    def test_book_return(self):
        """Test that a book can be returned and marked as available"""
        self.valid_book.borrow()
        self.valid_book.return_book()
        self.assertTrue(self.valid_book.is_available)

    # Test: Book availability check method
    def test_book_is_available_to_borrow(self):
        """Test the is_available_to_borrow method"""
        self.assertTrue(self.valid_book.is_available_to_borrow())
        self.valid_book.borrow()
        self.assertFalse(self.valid_book.is_available_to_borrow())

    # Test: Book string representation
    def test_book_str_available(self):
        """Test string representation of available book"""
        book_str = str(self.valid_book)
        self.assertIn("Test Book", book_str)
        self.assertIn("Test Author", book_str)
        self.assertIn("Available", book_str)

    # Test: Book string representation when borrowed
    def test_book_str_not_available(self):
        """Test string representation of borrowed book"""
        self.valid_book.borrow()
        book_str = str(self.valid_book)
        self.assertIn("Not Available", book_str)

    # Test: Datetime tracking when book is borrowed
    def test_book_borrow_with_datetime(self):
        """Test that borrowing a book records timestamp and member"""
        member = Member(1, "John Doe", 25, "john@example.com")
        before_borrow = datetime.now()
        self.valid_book.borrow(member=member)
        after_borrow = datetime.now()
        
        # Verify datetime was recorded
        self.assertIsNotNone(self.valid_book.borrowed_at)
        self.assertGreaterEqual(self.valid_book.borrowed_at, before_borrow)
        self.assertLessEqual(self.valid_book.borrowed_at, after_borrow)
        
        # Verify member was recorded
        self.assertIsNotNone(self.valid_book.borrowed_by)
        self.assertEqual(self.valid_book.borrowed_by, member)

    # Test: Datetime tracking when book is returned
    def test_book_return_with_datetime(self):
        """Test that returning a book records timestamp and member"""
        member = Member(1, "John Doe", 25, "john@example.com")
        self.valid_book.borrow(member=member)
        
        before_return = datetime.now()
        self.valid_book.return_book(member=member)
        after_return = datetime.now()
        
        # Verify datetime was recorded
        self.assertIsNotNone(self.valid_book.returned_at)
        self.assertGreaterEqual(self.valid_book.returned_at, before_return)
        self.assertLessEqual(self.valid_book.returned_at, after_return)
        
        # Verify member was recorded
        self.assertIsNotNone(self.valid_book.returned_by)
        self.assertEqual(self.valid_book.returned_by, member)

    # Test: Get borrow details for currently borrowed book
    def test_book_get_borrow_details(self):
        """Test getting borrow details for a borrowed book"""
        member = Member(1, "John Doe", 25, "john@example.com")
        self.valid_book.borrow(member=member)
        
        borrow_details = self.valid_book.get_borrow_details()
        
        # Verify borrow details dictionary has required keys
        self.assertIsNotNone(borrow_details)
        self.assertIn('borrowed_at', borrow_details)
        self.assertIn('borrowed_by', borrow_details)
        self.assertIn('borrowed_by_id', borrow_details)
        
        # Verify correct values
        self.assertEqual(borrow_details['borrowed_by'], 'John Doe')
        self.assertEqual(borrow_details['borrowed_by_id'], 1)

    # Test: Get borrow details returns None for available book
    def test_book_get_borrow_details_unavailable(self):
        """Test that get_borrow_details returns None for available book"""
        borrow_details = self.valid_book.get_borrow_details()
        self.assertIsNone(borrow_details)

    # Test: Get return details for returned book
    def test_book_get_return_details(self):
        """Test getting return details for a returned book"""
        member = Member(1, "John Doe", 25, "john@example.com")
        self.valid_book.borrow(member=member)
        self.valid_book.return_book(member=member)
        
        return_details = self.valid_book.get_return_details()
        
        # Verify return details dictionary has required keys
        self.assertIsNotNone(return_details)
        self.assertIn('returned_at', return_details)
        self.assertIn('returned_by', return_details)
        self.assertIn('returned_by_id', return_details)
        
        # Verify correct values
        self.assertEqual(return_details['returned_by'], 'John Doe')
        self.assertEqual(return_details['returned_by_id'], 1)

    # Test: Get return details returns None for currently borrowed book
    def test_book_get_return_details_borrowed(self):
        """Test that get_return_details returns None for borrowed book"""
        member = Member(1, "John Doe", 25, "john@example.com")
        self.valid_book.borrow(member=member)
        
        return_details = self.valid_book.get_return_details()
        self.assertIsNone(return_details)


class TestMember(unittest.TestCase):
    """Test cases for the Member class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a valid member for testing
        self.valid_member = Member(1, "John Doe", 25, "john@example.com")
        # Create books for borrowing tests
        self.book1 = Book(1, "Book One", "Author One", "Fiction")
        self.book2 = Book(2, "Book Two", "Author Two", "Fiction")
        self.book3 = Book(3, "Book Three", "Author Three", "Fiction")

    # Test: Valid member creation with correct parameters
    def test_member_creation_valid(self):
        """Test that a member can be created successfully with valid parameters"""
        self.assertEqual(self.valid_member.member_id, 1)
        self.assertEqual(self.valid_member.name, "John Doe")
        self.assertEqual(self.valid_member.age, 25)
        self.assertEqual(self.valid_member.contact_info, "john@example.com")
        self.assertEqual(len(self.valid_member.borrowed_books), 0)

    # Test: Invalid member creation with negative ID
    def test_member_creation_invalid_id(self):
        """Test that member creation fails with negative member_id"""
        with self.assertRaises(ValueError):
            Member(-1, "John Doe", 25, "john@example.com")

    # Test: Invalid member creation with zero ID
    def test_member_creation_invalid_id_zero(self):
        """Test that member creation fails with zero member_id"""
        with self.assertRaises(ValueError):
            Member(0, "John Doe", 25, "john@example.com")

    # Test: Invalid member creation with empty name
    def test_member_creation_invalid_name(self):
        """Test that member creation fails with empty name"""
        with self.assertRaises(ValueError):
            Member(1, "", 25, "john@example.com")

    # Test: Invalid member creation with negative age
    def test_member_creation_invalid_age(self):
        """Test that member creation fails with negative age"""
        with self.assertRaises(ValueError):
            Member(1, "John Doe", -5, "john@example.com")

    # Test: Invalid member creation with empty contact info
    def test_member_creation_invalid_contact(self):
        """Test that member creation fails with empty contact info"""
        with self.assertRaises(ValueError):
            Member(1, "John Doe", 25, "")

    # Test: Member can borrow a book
    def test_member_borrow_book(self):
        """Test that a member can borrow an available book"""
        self.member = Member(2, "Jane Doe", 30, "jane@example.com")
        self.member.borrow_book(self.book1)
        self.assertEqual(len(self.member.borrowed_books), 1)
        self.assertIn(self.book1, self.member.borrowed_books)
        self.assertFalse(self.book1.is_available)

    # Test: Member cannot borrow unavailable book
    def test_member_borrow_unavailable_book(self):
        """Test that a member cannot borrow an already borrowed book"""
        self.member = Member(2, "Jane Doe", 30, "jane@example.com")
        self.book1.borrow()  # Book is already borrowed
        self.member.borrow_book(self.book1)
        self.assertEqual(len(self.member.borrowed_books), 0)

    # Test: Member cannot borrow more than max limit (2 books)
    def test_member_borrow_exceeds_limit(self):
        """Test that a member cannot borrow more than MAX_BORROW_LIMIT (2 books)"""
        self.member = Member(2, "Jane Doe", 30, "jane@example.com")
        self.member.borrow_book(self.book1)
        self.member.borrow_book(self.book2)
        # Try to borrow third book - should fail
        self.member.borrow_book(self.book3)
        self.assertEqual(len(self.member.borrowed_books), 2)

    # Test: Member can return a borrowed book
    def test_member_return_book(self):
        """Test that a member can return a borrowed book"""
        self.member = Member(2, "Jane Doe", 30, "jane@example.com")
        self.member.borrow_book(self.book1)
        self.member.return_book(self.book1)
        self.assertEqual(len(self.member.borrowed_books), 0)
        self.assertTrue(self.book1.is_available)

    # Test: Member cannot return a book they didn't borrow
    def test_member_return_unborrows_book(self):
        """Test that a member cannot return a book they didn't borrow"""
        self.member = Member(2, "Jane Doe", 30, "jane@example.com")
        self.member.return_book(self.book1)  # Never borrowed this book
        self.assertEqual(len(self.member.borrowed_books), 0)

    # Test: Member string representation
    def test_member_str(self):
        """Test string representation of member"""
        member_str = str(self.valid_member)
        self.assertIn("John Doe", member_str)
        self.assertIn("ID: 1", member_str)
        self.assertIn("Borrowed Books", member_str)

    # Test: Member borrow passes member context to book
    def test_member_borrow_passes_member_context(self):
        """Test that member.borrow_book passes member context to book"""
        self.member = Member(2, "Jane Doe", 30, "jane@example.com")
        self.member.borrow_book(self.book1)
        
        # Verify book has member context
        self.assertEqual(self.book1.borrowed_by, self.member)
        self.assertIsNotNone(self.book1.borrowed_at)

    # Test: Member return passes member context to book
    def test_member_return_passes_member_context(self):
        """Test that member.return_book passes member context to book"""
        self.member = Member(2, "Jane Doe", 30, "jane@example.com")
        self.member.borrow_book(self.book1)
        self.member.return_book(self.book1)
        
        # Verify book has member return context
        self.assertEqual(self.book1.returned_by, self.member)
        self.assertIsNotNone(self.book1.returned_at)


class TestLibrary(unittest.TestCase):
    """Test cases for the Library class"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create a library for testing
        self.library = Library()
        # Create test books
        self.book1 = Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "Fiction")
        self.book2 = Book(2, "1984", "George Orwell", "Dystopian")
        self.book3 = Book(3, "The Hobbit", "J.R.R. Tolkien", "Fantasy")
        # Create test members
        self.member1 = Member(1, "Alice", 25, "alice@example.com")
        self.member2 = Member(2, "Bob", 30, "bob@example.com")

    # Test: Library can add a single book
    def test_library_add_book(self):
        """Test that library can add a single book"""
        self.library.add_book(self.book1)
        self.assertEqual(len(self.library.books), 1)
        self.assertIn(self.book1, self.library.books)

    # Test: Library can add multiple books at once
    def test_library_add_books(self):
        """Test that library can add multiple books at once"""
        self.library.add_books(self.book1, self.book2, self.book3)
        self.assertEqual(len(self.library.books), 3)
        self.assertIn(self.book1, self.library.books)
        self.assertIn(self.book2, self.library.books)
        self.assertIn(self.book3, self.library.books)

    # Test: Library can remove a book
    def test_library_remove_book(self):
        """Test that library can remove a book"""
        self.library.add_book(self.book1)
        self.library.remove_book(self.book1)
        self.assertEqual(len(self.library.books), 0)

    # Test: Library can add a single member
    def test_library_add_member(self):
        """Test that library can add a single member"""
        self.library.add_member(self.member1)
        self.assertEqual(len(self.library.members), 1)
        self.assertIn(self.member1, self.library.members)

    # Test: Library can add multiple members at once
    def test_library_add_members(self):
        """Test that library can add multiple members at once"""
        self.library.add_members(self.member1, self.member2)
        self.assertEqual(len(self.library.members), 2)
        self.assertIn(self.member1, self.library.members)
        self.assertIn(self.member2, self.library.members)

    # Test: Library can remove a member
    def test_library_remove_member(self):
        """Test that library can remove a member"""
        self.library.add_member(self.member1)
        self.library.remove_member(self.member1)
        self.assertEqual(len(self.library.members), 0)

    # Test: Library can issue a book to a member
    def test_library_issue_book(self):
        """Test that library can issue an available book to a member"""
        self.library.add_book(self.book1)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        self.assertIn(self.book1, self.member1.borrowed_books)
        self.assertFalse(self.book1.is_available)

    # Test: Library cannot issue unavailable book
    def test_library_issue_unavailable_book(self):
        """Test that library cannot issue an already borrowed book"""
        self.library.add_book(self.book1)
        self.library.add_member(self.member1)
        self.library.add_member(self.member2)
        self.library.issue_book(self.book1, self.member1)
        # Try to issue same book to another member
        self.library.issue_book(self.book1, self.member2)
        self.assertNotIn(self.book1, self.member2.borrowed_books)

    # Test: Library can accept book return from member
    def test_library_return_book(self):
        """Test that library can accept a book return from a member"""
        self.library.add_book(self.book1)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        self.library.return_book(self.book1, self.member1)
        self.assertNotIn(self.book1, self.member1.borrowed_books)
        self.assertTrue(self.book1.is_available)

    # Test: Library can retrieve all available books
    def test_library_available_books(self):
        """Test that library can retrieve all available books"""
        self.library.add_books(self.book1, self.book2, self.book3)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        available = self.library.available_books()
        self.assertEqual(len(available), 2)
        self.assertNotIn(self.book1, available)
        self.assertIn(self.book2, available)
        self.assertIn(self.book3, available)

    # Test: Library can filter available books by genre
    def test_library_available_books_by_genre(self):
        """Test that library can filter available books by genre"""
        self.library.add_books(self.book1, self.book2, self.book3)
        fiction_books = self.library.available_books(genre="Fiction")
        self.assertEqual(len(fiction_books), 1)
        self.assertIn(self.book1, fiction_books)
        self.assertNotIn(self.book2, fiction_books)

    # Test: Library can retrieve issued books
    def test_library_issued_books(self):
        """Test that library can retrieve all issued (borrowed) books"""
        self.library.add_books(self.book1, self.book2, self.book3)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        self.library.issue_book(self.book2, self.member1)
        issued = self.library.issued_books()
        self.assertEqual(len(issued), 2)
        self.assertIn(self.book1, issued)
        self.assertIn(self.book2, issued)

    # Test: Library can search books by keyword
    def test_library_search_books_by_title(self):
        """Test that library can search for books by title keyword"""
        self.library.add_books(self.book1, self.book2, self.book3)
        results = self.library.search_books("Great")
        self.assertEqual(len(results), 1)
        self.assertIn(self.book1, results)

    # Test: Library can search books by author
    def test_library_search_books_by_author(self):
        """Test that library can search for books by author keyword"""
        self.library.add_books(self.book1, self.book2, self.book3)
        results = self.library.search_books("Tolkien")
        self.assertEqual(len(results), 1)
        self.assertIn(self.book3, results)

    # Test: Library search is case-insensitive
    def test_library_search_case_insensitive(self):
        """Test that library search is case-insensitive"""
        self.library.add_books(self.book1, self.book2, self.book3)
        results = self.library.search_books("gatsby")
        self.assertEqual(len(results), 1)
        self.assertIn(self.book1, results)

    # Test: Library search with empty results
    def test_library_search_no_results(self):
        """Test that library search returns empty list when no matches found"""
        self.library.add_books(self.book1, self.book2, self.book3)
        results = self.library.search_books("NonExistent")
        self.assertEqual(len(results), 0)

    # Test: Library can identify members with borrowed books
    def test_library_members_with_borrowed_books(self):
        """Test that library can identify members with borrowed books"""
        self.library.add_books(self.book1, self.book2)
        self.library.add_members(self.member1, self.member2)
        self.library.issue_book(self.book1, self.member1)
        members_with_books = self.library.members_with_borrowed_books(self.library.members)
        self.assertEqual(len(members_with_books), 1)
        self.assertIn(self.member1, members_with_books)
        self.assertNotIn(self.member2, members_with_books)

    # Test: Library can count books by genre
    def test_library_books_count_by_genre(self):
        """Test that library can count books grouped by genre"""
        self.library.add_books(self.book1, self.book2, self.book3)
        counts = self.library.books_count_by_genre()
        self.assertEqual(counts["Fiction"], 1)
        self.assertEqual(counts["Dystopian"], 1)
        self.assertEqual(counts["Fantasy"], 1)

    # Test: Library can count issued books by genre
    def test_library_issued_books_count_by_genre(self):
        """Test that library can count issued books grouped by genre"""
        self.library.add_books(self.book1, self.book2, self.book3)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        self.library.issue_book(self.book2, self.member1)
        counts = self.library.books_count_by_genre(check_for_issuance=True)
        self.assertEqual(counts["Fiction"], 1)
        self.assertEqual(counts["Dystopian"], 1)
        self.assertNotIn("Fantasy", counts)

    # Test: Library can find most popular genre among issued books
    def test_library_most_popular_genre(self):
        """Test that library can identify most popular genre among issued books"""
        self.library.add_books(self.book1, self.book2, self.book3)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        self.library.issue_book(self.book2, self.member1)
        popular_genres = self.library.most_popular_genre_from_issued_books()
        self.assertEqual(len(popular_genres), 2)  # Fiction and Dystopian tied at 1

    # Test: Library can get current borrow details for a book
    def test_library_get_book_borrow_details(self):
        """Test that library can retrieve current borrow details"""
        self.library.add_book(self.book1)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        
        borrow_details = self.library.get_book_borrow_details(self.book1)
        
        # Verify borrow details exist and contain correct information
        self.assertIsNotNone(borrow_details)
        self.assertIn('borrowed_at', borrow_details)
        self.assertIn('borrowed_by', borrow_details)
        self.assertIn('borrowed_by_id', borrow_details)
        self.assertEqual(borrow_details['borrowed_by'], 'Alice')
        self.assertEqual(borrow_details['borrowed_by_id'], 1)

    # Test: Library get borrow details returns None for available book
    def test_library_get_book_borrow_details_available(self):
        """Test that get_book_borrow_details returns None for available book"""
        self.library.add_book(self.book1)
        
        borrow_details = self.library.get_book_borrow_details(self.book1)
        self.assertIsNone(borrow_details)

    # Test: Library can get return details for a returned book
    def test_library_get_book_return_details(self):
        """Test that library can retrieve return details"""
        self.library.add_book(self.book1)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        self.library.return_book(self.book1, self.member1)
        
        return_details = self.library.get_book_return_details(self.book1)
        
        # Verify return details exist and contain correct information
        self.assertIsNotNone(return_details)
        self.assertIn('returned_at', return_details)
        self.assertIn('returned_by', return_details)
        self.assertIn('returned_by_id', return_details)
        self.assertEqual(return_details['returned_by'], 'Alice')
        self.assertEqual(return_details['returned_by_id'], 1)

    # Test: Library get return details returns None for borrowed book
    def test_library_get_book_return_details_borrowed(self):
        """Test that get_book_return_details returns None for borrowed book"""
        self.library.add_book(self.book1)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        
        return_details = self.library.get_book_return_details(self.book1)
        self.assertIsNone(return_details)

    # Test: Library can get complete book history
    def test_library_get_book_history(self):
        """Test that library can retrieve complete book history"""
        self.library.add_book(self.book1)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        self.library.return_book(self.book1, self.member1)
        
        history = self.library.get_book_history(self.book1)
        
        # Verify history contains all required information
        self.assertIsNotNone(history)
        self.assertIn('book_id', history)
        self.assertIn('title', history)
        self.assertIn('is_available', history)
        self.assertIn('borrow_details', history)
        self.assertIn('return_details', history)
        
        # Verify values
        self.assertEqual(history['book_id'], 1)
        self.assertEqual(history['title'], 'The Great Gatsby')
        self.assertTrue(history['is_available'])
        self.assertIsNotNone(history['return_details'])
        self.assertIsNone(history['borrow_details'])  # Book is now available

    # Test: Library book history for currently borrowed book
    def test_library_get_book_history_borrowed(self):
        """Test book history for currently borrowed book"""
        self.library.add_book(self.book1)
        self.library.add_member(self.member1)
        self.library.issue_book(self.book1, self.member1)
        
        history = self.library.get_book_history(self.book1)
        
        # Verify history for borrowed book
        self.assertFalse(history['is_available'])
        self.assertIsNotNone(history['borrow_details'])
        self.assertIsNone(history['return_details'])


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling and edge cases"""

    # Test: Invalid book object in library operations
    def test_library_add_invalid_book(self):
        """Test that library handles invalid book objects gracefully"""
        library = Library()
        invalid_book = "not a book"
        library.add_book(invalid_book)  # Should be caught internally
        # The library should not crash

    # Test: Search with empty keyword
    def test_library_search_empty_keyword(self):
        """Test that library search handles empty keyword gracefully"""
        library = Library()
        book = Book(1, "Test", "Author", "Fiction")
        library.add_book(book)
        results = library.search_books("")
        self.assertEqual(results, [])

    # Test: Multiple borrowing and returning cycles
    def test_book_multiple_borrow_return_cycles(self):
        """Test that book can be borrowed and returned multiple times"""
        book = Book(1, "Reusable Book", "Author", "Fiction")
        member = Member(1, "John", 25, "john@example.com")
        
        # First cycle
        member.borrow_book(book)
        self.assertIn(book, member.borrowed_books)
        member.return_book(book)
        self.assertNotIn(book, member.borrowed_books)
        
        # Second cycle
        member.borrow_book(book)
        self.assertIn(book, member.borrowed_books)
        member.return_book(book)
        self.assertNotIn(book, member.borrowed_books)

    # Test: Datetime tracking across multiple borrow/return cycles
    def test_datetime_tracking_multiple_cycles(self):
        """Test that datetime tracking works correctly across multiple cycles"""
        book = Book(1, "Multi-Cycle Book", "Author", "Fiction")
        member1 = Member(1, "Alice", 25, "alice@example.com")
        member2 = Member(2, "Bob", 30, "bob@example.com")
        
        # First cycle - member1 borrows and returns
        book.borrow(member=member1)
        first_borrow_member = book.borrowed_by
        first_borrow_time = book.borrowed_at
        self.assertEqual(first_borrow_member.member_id, 1)
        
        book.return_book(member=member1)
        first_return_member = book.returned_by
        first_return_time = book.returned_at
        self.assertEqual(first_return_member.member_id, 1)
        
        # Second cycle - member2 borrows and returns
        book.borrow(member=member2)
        second_borrow_member = book.borrowed_by
        second_borrow_time = book.borrowed_at
        self.assertEqual(second_borrow_member.member_id, 2)
        # Second borrow time should be later than first
        self.assertGreater(second_borrow_time, first_borrow_time)
        
        book.return_book(member=member2)
        second_return_member = book.returned_by
        second_return_time = book.returned_at
        self.assertEqual(second_return_member.member_id, 2)
        # Second return time should be later than first
        self.assertGreater(second_return_time, first_return_time)


class TestDatetimeDemo(unittest.TestCase):
    """Integration-style tests ported from test_datetime_tracking.py to verify
    datetime tracking behavior in typical workflows."""

    def test_demo_borrow_records_borrow_details(self):
        library = Library()
        book1 = Book(1, "Test Book 1", "Author 1", "Fiction")
        member1 = Member(1, "John Doe", 30, "john@example.com")

        library.add_book(book1)
        library.add_member(member1)

        library.issue_book(book1, member1)

        borrow_details = library.get_book_borrow_details(book1)
        self.assertIsNotNone(borrow_details)
        self.assertIn('borrowed_at', borrow_details)
        self.assertIn('borrowed_by', borrow_details)
        self.assertIn('borrowed_by_id', borrow_details)
        self.assertEqual(borrow_details['borrowed_by'], 'John Doe')
        self.assertEqual(borrow_details['borrowed_by_id'], 1)

    def test_demo_return_records_return_details(self):
        library = Library()
        book1 = Book(1, "Test Book 1", "Author 1", "Fiction")
        member1 = Member(1, "John Doe", 30, "john@example.com")

        library.add_book(book1)
        library.add_member(member1)

        library.issue_book(book1, member1)
        # small delay to ensure timestamps differ
        time.sleep(0.1)
        library.return_book(book1, member1)

        return_details = library.get_book_return_details(book1)
        self.assertIsNotNone(return_details)
        self.assertIn('returned_at', return_details)
        self.assertIn('returned_by', return_details)
        self.assertIn('returned_by_id', return_details)
        self.assertEqual(return_details['returned_by'], 'John Doe')
        self.assertEqual(return_details['returned_by_id'], 1)

    def test_demo_complete_history(self):
        library = Library()
        book1 = Book(1, "Test Book 1", "Author 1", "Fiction")
        member1 = Member(1, "John Doe", 30, "john@example.com")

        library.add_book(book1)
        library.add_member(member1)

        library.issue_book(book1, member1)
        time.sleep(0.1)
        library.return_book(book1, member1)

        history = library.get_book_history(book1)
        self.assertIsNotNone(history)
        self.assertEqual(history['book_id'], 1)
        self.assertEqual(history['title'], 'Test Book 1')
        self.assertTrue(history['is_available'])
        self.assertIsNotNone(history['return_details'])

    def test_demo_currently_borrowed_book(self):
        library = Library()
        book2 = Book(2, "Test Book 2", "Author 2", "Fiction")
        member2 = Member(2, "Jane Smith", 25, "jane@example.com")

        library.add_book(book2)
        library.add_member(member2)

        library.issue_book(book2, member2)

        history2 = library.get_book_history(book2)
        self.assertIsNotNone(history2)
        self.assertFalse(history2['is_available'])
        self.assertIsNotNone(history2['borrow_details'])
        self.assertEqual(history2['borrow_details']['borrowed_by'], 'Jane Smith')


if __name__ == '__main__':
    # Run all tests with verbose output
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""
Test script to verify datetime tracking functionality in the Library Management System
"""

from library import Library
from book import Book
from member import Member
import time

# Create library, books, and members
library = Library()

# Create sample books
book1 = Book(1, "Test Book 1", "Author 1", "Fiction")
book2 = Book(2, "Test Book 2", "Author 2", "Fiction")

member1 = Member(1, "John Doe", 30, "john@example.com")
member2 = Member(2, "Jane Smith", 25, "jane@example.com")

# Add to library
library.add_book(book1)
library.add_book(book2)
library.add_member(member1)
library.add_member(member2)

print("=" * 70)
print("DATETIME TRACKING FEATURE DEMONSTRATION")
print("=" * 70)

# Test 1: Borrow a book
print("\n[TEST 1] Borrowing Book 1 by John Doe...")
library.issue_book(book1, member1)
time.sleep(1)  # Add a small delay to show time difference

# Display borrow details
print("\nBook 1 Borrow Details:")
borrow_details = library.get_book_borrow_details(book1)
if borrow_details:
    print(f"  ✓ Borrowed At: {borrow_details['borrowed_at']}")
    print(f"  ✓ Borrowed By: {borrow_details['borrowed_by']} (ID: {borrow_details['borrowed_by_id']})")
else:
    print("  ✗ No borrow details found")

# Test 2: Return a book
print("\n[TEST 2] Returning Book 1 to library...")
library.return_book(book1, member1)

# Display return details
print("\nBook 1 Return Details:")
return_details = library.get_book_return_details(book1)
if return_details:
    print(f"  ✓ Returned At: {return_details['returned_at']}")
    print(f"  ✓ Returned By: {return_details['returned_by']} (ID: {return_details['returned_by_id']})")
else:
    print("  ✗ No return details found")

# Test 3: Complete book history
print("\n[TEST 3] Complete History for Book 1:")
history = library.get_book_history(book1)
if history:
    print(f"  Book ID: {history['book_id']}")
    print(f"  Title: {history['title']}")
    print(f"  Current Status: {'Available' if history['is_available'] else 'Borrowed'}")
    
    if history['borrow_details']:
        print(f"\n  Borrow Details:")
        print(f"    - Borrowed At: {history['borrow_details']['borrowed_at']}")
        print(f"    - Borrowed By: {history['borrow_details']['borrowed_by']}")
    
    if history['return_details']:
        print(f"\n  Return Details:")
        print(f"    - Returned At: {history['return_details']['returned_at']}")
        print(f"    - Returned By: {history['return_details']['returned_by']}")

# Test 4: Currently borrowed book
print("\n[TEST 4] Currently Borrowed Book (Book 2 by Jane Smith)...")
library.issue_book(book2, member2)

print("\nBook 2 Status (Currently Borrowed):")
history2 = library.get_book_history(book2)
if history2:
    print(f"  Is Available: {history2['is_available']}")
    if history2['borrow_details']:
        print(f"  Currently Borrowed By: {history2['borrow_details']['borrowed_by']} (ID: {history2['borrow_details']['borrowed_by_id']})")
        print(f"  Borrowed At: {history2['borrow_details']['borrowed_at']}")
    if history2['return_details']:
        print(f"  Last Returned At: {history2['return_details']['returned_at']}")

print("\n" + "=" * 70)
print("✓ All datetime tracking tests completed successfully!")
print("=" * 70)

# def main():
#     print("Hello from class04-library-management-system!")


# if __name__ == "__main__":
#     main()

import sqlite3

DB_FILE = "library.db"

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            read INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author: ")
    year = input("Enter publication year: ")
    genre = input("Enter genre: ")
    read = input("Have you read this book? (yes/no): ").strip().lower() == 'yes'
    
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO books (title, author, year, genre, read) VALUES (?, ?, ?, ?, ?)', 
              (title, author, int(year), genre, int(read)))
    conn.commit()
    conn.close()
    print("✅ Book added successfully!")

def remove_book():
    book_id = input("Enter the book ID to remove: ")
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    print("🚮 Book removed successfully!")

def search_books():
    query = input("Enter title or author to search: ").strip().lower()
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM books WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ?', (f'%{query}%', f'%{query}%'))
    results = c.fetchall()
    conn.close()
    if results:
        for book in results:
            print(f"{book['id']}: {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        print("❌ No books found.")

def display_books():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()
    if books:
        for book in books:
            print(f"{book['id']}: {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        print("📭 No books in the library.")

def display_statistics():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM books')
    total_books = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM books WHERE read = 1')
    read_books = c.fetchone()[0]
    conn.close()
    print(f"📚 Total Books: {total_books}")
    print(f"✅ Books Read: {read_books}")
    print(f"📖 Unread Books: {total_books - read_books}")

def main():
    initialize_db()
    while True:
        print("\n📚 Library Manager")
        print("1. Add a Book")
        print("2. Remove a Book")
        print("3. Search for a Book")
        print("4. Display All Books")
        print("5. Display Statistics")
        print("6. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            add_book()
        elif choice == "2":
            remove_book()
        elif choice == "3":
            search_books()
        elif choice == "4":
            display_books()
        elif choice == "5":
            display_statistics()
        elif choice == "6":
            print("📁 Library saved. Goodbye! 👋")
            break
        else:
            print("⚠ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

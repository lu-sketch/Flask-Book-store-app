import sqlite3

def create_table():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ebooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Author TEXT NOT NULL,
        Qty INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def populate_table():
    books = [
        ('A Tale of Two Cities', 'Charles Dickens', 30),
        ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
        ('The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 21),
        ('The Lord of the Rings', 'J.R.R. Tolkien', 37),
        ('Alice in Wonderland', 'Lewis Carroll', 12),
        ('Pillars of the Earth', 'Ken Follett', 25)
    ]

    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO ebooks (Title, Author, Qty) VALUES (?, ?, ?)', books)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
    populate_table()
    print("Database initialized and populated successfully.")

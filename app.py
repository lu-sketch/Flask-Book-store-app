from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b33km8nger'  


# Establish connection to the database
def get_db_connection():
    """Connect to the database"""
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn



@app.route('/')
def index():
    """Index of the application first html page - index"""
    current_year = datetime.now().year
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM ebooks').fetchall()
    conn.close()

    return render_template('index.html', books=books, current_year=current_year)



@app.route('/add', methods=('GET', 'POST'))
def add():
    """This function will enable the user to add a book to the database"""
    current_year = datetime.now().year
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        qty = request.form['qty']

        conn = get_db_connection()
        conn.execute('INSERT INTO ebooks (Title, Author, Qty) VALUES (?, ?, ?)', 
                     (title, author, qty))
        conn.commit()
        conn.close()
    
        return redirect(url_for('index'))
    return render_template('add.html', current_year=current_year)



@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    """Here a user can update information for specific books in the database"""
    conn = get_db_connection()
    current_year = datetime.now().year 
    book = conn.execute('SELECT * FROM ebooks WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        qty = request.form['qty']

        conn.execute('UPDATE ebooks SET Title = ?, Author = ?, Qty = ? WHERE id = ?',
                     (title, author, qty, id))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('update.html', book=book, current_year=current_year)


@app.route('/search', methods=('GET', 'POST'))
def search():
    """By entering a book ID the user can search for books"""
    book = None
    current_year = datetime.now().year
    if request.method == 'POST':
        book_id = request.form['id']
        conn = get_db_connection()
        book = conn.execute('SELECT * FROM ebooks WHERE id = ?', (book_id,)).fetchone()
        conn.close()
    
        if not book:
            flash('Book not found!', 'error')
    return render_template('search.html', book=book,current_year=current_year)



@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    """Here the user can delete a book from the database."""
    current_year = datetime.now().year
    conn = get_db_connection()
    conn.execute('DELETE FROM ebooks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'), current_year=current_year)




if __name__ == "__main__":
    app.run(debug=True)


#============================================THE END================================


import os
import urllib

from flask import Flask, render_template, url_for, request, flash, redirect

app = Flask(__name__)

from sqlalchemy import and_, or_, not_
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

# use a constant here, so that the same bases is used for all tables
# Now save this schema information to the database
from EntitiesAsClasses import Author, Customer, Book, Publisher, Rating, Restock, Transaction
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

# Your Rowan username
username = 'carberryt9'

# The password to the database. Not your Rowan password!
password = 'password1'
# ON ELVIS
connection = create_engine('mysql+pymysql://' + username + ':' + password + '@elvis.rowan.edu/' + username)
# ON LOCAL
# connection = create_engine('mysql+pymysql://'+'username:password'+':@localhost:3306/'+'schemaName')
BASE.metadata.create_all(connection)

# create a session that we can use to interact with the database
Session = sessionmaker(bind=connection)
# create a session for our use from our generated Session class.
session = Session()


@app.route('/')
def hello_world():
    return "<h1>Welcome to Rowan Bookstore</h1>" \
           "<p><a href='/categories'> Shop</a></p>" \
           "<p><a href='/book'> View All Books</a></p>" \
           "<p><a href='/author'> View All Authors</a></p>" \
           "<p><a href='/publisher'> View All Publishers</a></p>"


@app.route('/book')
def all_books():
    books = session.query(Book.Book).all()
    return render_template('booklist.html',
                           books=books,
                           title='All Books')


@app.route('/book/<int:bookId>/')
def one_book(bookId):
    book = session.query(Book.Book).filter_by(book_id=bookId).one()
    return render_template('book.html',
                           book=book,
                           title=book.title)


@app.route('/book/modify/<int:bookId>/', methods=['GET', 'POST'])
def modify_book(bookId):
    book = session.query(Book.Book).filter_by(book_id=bookId).one()
    if request.method == 'POST':
        book.title = request.form['title']
        book.description = request.form['description']
        book.pages = request.form['pages']
        #book.release_year = request.form['release_year']
        #book.price = request.form['price']
        #book.publisher_id = request.form['publisher_id']
        #session.
        session.add(book)
        session.commit()
        flash(book.title + "'s information updated")
        return redirect(url_for('all_books'))
    else:
        return render_template('editBook.html', book=book)


@app.route('/book/delete/<int:book_id>/', methods=['GET', 'POST'])
def delete_book(book_id):
    book = session.query(Book.Book).filter_by(book_id=book_id).one()
    if request.method == 'POST':
        session.delete(book)
        session.commit()
        flash(book.title + " deleted")
        return redirect(url_for('all_books'))
    else:
        return render_template('deleteBook.html', book=book)


@app.route('/book/new/', methods=['GET', 'POST'])
def insert_book():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        num_in_stock = request.form['num_in_stock']
        pages = request.form['pages']
        release_year = request.form['release_year']
        price = request.form['price']
        # need to change author orm
        author_id = session.query(Author.Author).filter_by(author_id = request.form['author_id']).one()
        newBook = Book.Book(title=title, description=description, num_in_stock=num_in_stock, pages=pages,
                            release_year=release_year, author_id = author_id, price = price)
        session.add(newBook)
        session.commit()
        flash("New book " + title + " created")
        return redirect(url_for('all_books'))
    else:
        return render_template('newBook.html')


@app.route('/publisher')
def all_publishers():
    print("Publishers:\n")
    publishers = session.query(Publisher.Publisher).all()
    print(publishers)
    html = '<h1> Publishers </h1>'
    for publisher in publishers:
        html += "<p><a href='/publisher/" + str(
            publisher.publisher_id) + "'> " + publisher.name + "</a></p>"
    return html


@app.route('/publisher/<int:publisherId>/')
def one_publisher(publisherId):
    print("Publisher:\n")
    publisher = session.query(Publisher.Publisher).filter_by(publisher_id=publisherId).one()
    print(publisher)
    html = '<h1>' + publisher.name + '</h1>'
    html += "<h2> Books: </h2>"

    for book in publisher.books:
        html += "<p><a href='/book/" + str(book.book_id) + "'> " + book.title + "</a></p>"
    return html


@app.route('/categories/', methods=['GET'])
def get_categories():
    categories = session.execute("SELECT name FROM all_categories ORDER BY name").fetchall()

    converted = []

    for cat in categories:
        it = dict(cat)
        it['encoded_name'] = urllib.parse.quote_plus(it['name'])
        converted.append(it)

    return render_template('categories.html', categories=converted)


@app.route('/specials/', methods=['GET'])
def get_specials():
    categories = session.execute("SELECT name FROM all_categories ORDER BY name").fetchall()

    converted = []

    for cat in categories:
        it = dict(cat)
        it['encoded_name'] = urllib.parse.quote_plus(it['name'])
        converted.append(it)

    return render_template('categories.html', categories=converted)


@app.route('/item/', methods=['GET'])
def get_all_items():
    category = request.args.get('category')
    if category is not None:
        all_items = session.execute('SELECT * FROM all_items WHERE category LIKE "%' + category + '%" ORDER BY name').fetchall()
    else:
        all_items = session.execute("SELECT * FROM all_items").fetchall()
    return render_template("items.html", items=all_items)


@app.route('/item/<string:item_id>/', methods=['GET'])
def get_specific_item(item_id):
    the_item = session.execute('SELECT * FROM all_items WHERE id="' + item_id + '"').fetchone()
    return render_template("item_details.html", item=the_item)




if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()

from flask import Flask

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
username = 'smithj1'

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
           "<p><a href='/book'> View All Books</a></p>" \
           "<p><a href='/author'> View All Authors</a></p>" \
           "<p><a href='/publisher'> View All Publishers</a></p>"


@app.route('/book')
def all_books():
    print("Books:\n")
    books = session.query(Book.Book).all()
    print(books)
    html = '<h1> Books </h1>'
    for book in books:
        html += "<p><a href='/book/" + str(book.book_id) + "'> " + book.title + "</a></p>"
    return html


@app.route('/author')
def all_authors():
    print("Authors:\n")
    authors = session.query(Author.Author).all()
    print(authors)
    html = '<h1> Authors </h1>'
    for author in authors:
        html += "<p><a href='/author/" + str(
            author.author_id) + "'> " + author.first_name + " " + author.last_name + "</a></p>"
    return html


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


@app.route('/book/<int:bookId>/')
def one_book(bookId):
    print("Book:\n")
    book = session.query(Book.Book).filter_by(book_id=bookId).one()
    print(book)
    html = '<h1>' + book.title + '</h1>'
    html += "<h2> Authors: </h2>"

    for author in book.authors:
        html += "<p><a href='/author/" + str(
            author.author_id) + "'> " + author.first_name + " " + author.last_name + "</a></p>"

    html += '<h2> Publisher </h2>'
    html += "<p><a href='/publisher/" + str(
        book.publisher_id) + "'> " + book.publisher.name + "</a></p>"
    return html


@app.route('/author/<int:authorId>/')
def one_author(authorId):
    print("Author:\n")
    author = session.query(Author.Author).filter_by(author_id=authorId).one()
    print(author)
    html = '<h1>' + author.first_name + " " + author.last_name + '</h1>'
    html += "<h2> Books: </h2>"

    for book in author.books:
        html += "<p><a href='/book/" + str(book.book_id) + "'> " + book.title + "</a></p>"
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


if __name__ == '__main__':
    app.run()

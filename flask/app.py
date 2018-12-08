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

current = ''

@app.route('/')
def hello_world():
    return "<h1>Welcome to Rowan Bookstore</h1>" \
           "<p><a href='/categories'> Shop</a></p>" \
           "<p><a href='/admin'> Admin</a></p>" \
           "<p><a href='/book'> View All Books</a></p>" \
           "<p><a href='/author'> View All Authors</a></p>" \
           "<p><a href='/publisher'> View All Publishers</a></p>"


# TODO: Make this a template
@app.route('/admin/')
def admin():
    global current
    current = 'admin'
    return "<h1>Welcome to Rowan Bookstore - Admin Page</h1>" \
           "<p><a href='/low_inventory'> Inventory that has fallen below the minimum stock level</a></p>" \
           "<p><a href='/when_ship'> When will orders ship?</a></p>" \
           "<p><a href='/never_bought'> Wish list but never bought</a></p>" \
           "<p><a href='/not_active_customers'> Not active customers</a></p>"


@app.route('/low_inventory/')
def low_inventory():
    inventory = session.execute(
        'SELECT title as name, concat("rowan_", book_id) as id FROM low_inventory ORDER BY title').fetchall()
    return render_template("items.html", items=inventory)


@app.route('/when_ship/')
def when_ship():
    day = session.execute(
        'SELECT day_of_week FROM when_will_order_ship').fetchone()
    return "Orders bought today will ship on " + day["day_of_week"]


@app.route('/not_active_customers/', methods=['GET'])
def not_active_customers():
    all_customers = session.execute("SELECT * FROM not_active_customers").fetchall()
    return render_template("customers.html", customers=all_customers)


@app.route('/book/')
def all_books():
    books = session.query(Book.Book).all()
    return render_template('booklist.html',
                           books=books,
                           title='All Books')


@app.route('/book/<int:bookId>/')
def one_book(bookId):
    book = session.query(Book.Book).filter_by(book_id=bookId).one()
    if current == 'admin':
        return render_template('book.html',
                           book=book,
                           title=book.title,
                           admin=current)
    else:
        return render_template('book.html',
                           book=book,
                           title=book.title,
                           user=current)


@app.route('/book/modify/<int:bookId>/', methods=['GET', 'POST'])
def modify_book(bookId):
    book = session.query(Book.Book).filter_by(book_id=bookId).one()
    if request.method == 'POST':
        book.title = request.form['title']
        book.description = request.form['description']
        book.pages = request.form['pages']
        # book.release_year = request.form['release_year']
        # book.price = request.form['price']
        # book.publisher_id = request.form['publisher_id']
        # session.
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
        author = session.query(Author.Author).filter_by(author_id = request.form['author_id']).one()
        print (author.author_id)
        newBook = Book.Book(title=title, description=description, num_in_stock=num_in_stock, pages=pages,
                            release_year=release_year, author=author, price=price)
        session.add(newBook)
        session.commit()
        flash("New book " + title + " created")
        return redirect(url_for('all_books'))
    else:
        authors = session.query(Author.Author).all()
        return render_template('newBook.html', authors=authors)


@app.route('/publisher/')
def all_publishers():
    publishers = session.query(Publisher.Publisher).all()
    return render_template('publisherlist.html',
                           publishers=publishers)


@app.route('/publisher/<int:publisherId>/')
def one_publisher(publisherId):
    publisher = session.query(Publisher.Publisher).filter_by(publisher_id=publisherId).one()
    return render_template('publisher.html',
                           publisher=publisher)

@app.route('/publisher/new/', methods=['GET','POST'])
def new_publisher():
    if request.method == 'POST':
        name=request.form['publisher_name']
        publisher = Publisher.Publisher(name)
        session.add(publisher)
        session.commit()
        flash("New publisher " + name + " created")
        return redirect(url_for('all_publishers'))
    else:
        return render_template('newPublisher.html')

@app.route('/publisher/modify/<int:publisherId>', methods=['GET','POST'])
def modify_publisher(publisherId):
    publisher = session.query(Publisher.Publisher).filter_by(publisher_id=publisherId).one()
    if request.method == 'POST':
        publisher.name=request.form['publisher_name']
        session.add(publisher)
        session.commit()
        flash("Publisher " + publisher.name + " edited")
        return redirect(url_for('all_publishers'))
    else:
        return render_template('editPublisher.html',
                               publisher=publisher)

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
    specials = session.execute(
        'SELECT * FROM specials ORDER BY name').fetchall()
    return render_template("items.html", items=specials)


@app.route('/item/', methods=['GET'])
def get_all_items():
    category = request.args.get('category')
    if category is not None:
        all_items = session.execute(
            'SELECT * FROM all_items WHERE category LIKE "%' + category + '%" ORDER BY name').fetchall()
    else:
        all_items = session.execute("SELECT * FROM all_items").fetchall()
    return render_template("items.html", items=all_items)


@app.route('/item/<string:item_id>/', methods=['GET'])
def get_specific_item(item_id):
    the_item = session.execute('SELECT * FROM all_items_with_rating WHERE id="' + item_id + '"').fetchone()
    return render_template("item_details.html", item=the_item)


@app.route('/customer/', methods=['GET'])
def get_all_customers():
    all_customers = session.execute("SELECT * FROM all_customers").fetchall()
    return render_template("customers.html", customers=all_customers)


@app.route('/never_bought/', methods=['GET'])
def wish_list_never_bought():
    never_bought = session.execute("SELECT * FROM wish_list_never_purchased").fetchall()
    return render_template("never_bought.html", never_bought=never_bought)


if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()

import os
import urllib
import time

from flask import Flask, render_template, url_for, request, flash, redirect

app = Flask(__name__)

from sqlalchemy import and_, or_, not_
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

# use a constant here, so that the same bases is used for all tables
# Now save this schema information to the database
from EntitiesAsClasses import Author, Customer, Book, Publisher, Rating, Restock, Transaction, Cart, Genre, WishList
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

current_user_id = 0

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/shop/')
def shop():
    global current_user_id
    current_user_id = 1
    return "<h1>Shop</h1>" \
           "<p><a href='/recommended'>Recommended for you</a></p>" \
           "<p><a href='/categories'>Shop By Category</a></p>" \
           "<p><a href='/wishlist'>View Wishlist</a></p>" \
           "<p><a href='/cart'>View Your Cart</a></p>"


# TODO: Make this a template
@app.route('/admin/')
def admin():
    global current_user_id
    current_user_id = 0
    return "<h1>Welcome to Rowan Bookstore - Admin Page</h1>" \
           "<p><a href='/low_inventory'> Inventory that has fallen below the minimum stock level</a></p>" \
           "<p><a href='/when_ship'> When will orders ship?</a></p>" \
           "<p><a href='/never_bought'> Wish list but never bought</a></p>" \
           "<p><a href='/not_active_customers'> Not active customers</a></p>" \
           "<br/>" \
           "<p><a href='/items_sold_day_of_week'>EXTRA CREDIT: Number of items sold per day of week</a></p>" \
           "<p><a href='/customers_spent_most'>EXTRA CREDIT:Customers who spent the most money</a></p>" \
           "<br/>" \
           "<p><a href='/book'>View All Books</a></p>" \
           "<p><a href='/author'>View All Authors</a></p>" \
           "<p><a href='/publisher'>View All Publishers</a></p>"



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

@app.route('/items_sold_day_of_week/', methods=['GET'])
def num_sold_day_week():
    num_sold_day_week = session.execute("SELECT * FROM items_sold_day_of_week").fetchall()
    return render_template("num_sold_day_of_week.html", num_sold_day_week=num_sold_day_week)


@app.route('/customers_spent_most/', methods=['GET'])
def customers_spent_most():
    customers_spent_most = session.execute("SELECT * FROM customers_spent_most").fetchall()
    return render_template("customers_spent_most.html", customers_spent_most=customers_spent_most)


@app.route('/book/')
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
                           title=book.title,
                           current_user_id=current_user_id)


@app.route('/book/modify/<int:book_id>/', methods=['GET', 'POST'])
def modify_book(book_id):
    book = session.query(Book.Book).filter_by(book_id=book_id).one()
    if request.method == 'POST':
        book.title = request.form['title']
        book.description = request.form['description']
        book.pages = request.form['pages']
        new_author_id = int(request.form['new_author'])
        if new_author_id != 0:
            author = session.query(Author.Author).filter_by(author_id=new_author_id).one()
            book.addAuthor(author)

        for author in book.authors:
            current_author_id = request.form['author_id_'+str(author.author_id)]
            if int(current_author_id) == 0:
                itemToBeDeleted = session.query(Author.Author_Book).filter_by(author_id=author.author_id, book_id=book.book_id).one()
                session.delete(itemToBeDeleted)
            else:
                session.query(Author.Author_Book).filter_by(author_id=author.author_id, book_id=book.book_id).update({"author_id":current_author_id})

        for genre in book.genres:
            current_genre_id = request.form['genre_id_'+str(genre.genre_id)]
            if int(current_author_id) == 0:
                itemToBeDeleted = session.query(Genre.Book_Genre).filter_by(genre_id=genre.genre_id, book_id=book.book_id).one()
                session.delete(itemToBeDeleted)
            else:
                session.query(Genre.Book_Genre).filter_by(genre_id=genre.genre_id, book_id=book.book_id).update({"genre_id":current_genre_id})

        book.release_year = request.form['release_year']
        book.price = request.form['price']
        book.num_in_stock = request.form['stock']
        # put this in if things break, also requires change to editBook.html
        # book.publisher_id = request.form['publisher_id']
        book.publisher.publisher_id = int(request.form['publisher_id'])
        session.add(book)
        session.commit()
        flash(book.title + "'s information updated")
        return redirect(url_for('all_books'))
    else:
        authors = get_all_authors()
        genres = get_all_genres()
        publishers = get_all_publishers()
        return render_template('editBook.html', book=book, allAuthors=authors, allGenres=genres, allPublishers=publishers)


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
        num_in_stock = request.form['stock']
        pages = request.form['pages']
        release_year = request.form['release_year']
        price = request.form['price']
        author = session.query(Author.Author).filter_by(author_id = request.form['author_id']).one()
        publisher = session.querry(Publisher.Publisher).filter_by(publisher_id = request.form['publisher_id']).one()
        genre = session.querry(Genre.Genre).filter_by(genre_id = request.form['genre_id']).one()
        newBook = Book.Book(title=title, description=description, num_in_stock=num_in_stock, pages=pages,
                            release_year=release_year, author=author, price=price,)
        session.add(newBook)
        session.commit()
        flash("New book " + title + " created")
        return redirect(url_for('all_books'))
    else:
        authors = get_all_authors()
        genres = get_all_genres()
        publishers = get_all_publishers()
        return render_template('newBook.html', authors=authors, genres=genres, publishers=publishers)


@app.route('/publisher/')
def all_publishers():
    publishers = session.query(Publisher.Publisher).all()
    return render_template('publisherlist.html',
                           publishers=publishers)


@app.route('/publisher/<int:publisher_id>/')
def one_publisher(publisher_id):
    publisher = session.query(Publisher.Publisher).filter_by(publisher_id=publisher_id).one()
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


@app.route('/publisher/modify/<int:publisher_id>', methods=['GET','POST'])
def modify_publisher(publisher_id):
    publisher = session.query(Publisher.Publisher).filter_by(publisher_id=publisher_id).one()
    if request.method == 'POST':
        publisher.name=request.form['publisher_name']
        session.add(publisher)
        session.commit()
        flash("Publisher " + publisher.name + " edited")
        return redirect(url_for('all_publishers'))
    else:
        return render_template('editPublisher.html',
                               publisher=publisher)


@app.route('/publisher/delete/<int:publisher_id>/', methods=['GET', 'POST'])
def delete_publisher(publisher_id):
    publisher = session.query(Publisher.Publisher).filter_by(publisher_id=publisher_id).one()
    if request.method == 'POST':
        session.delete(publisher)
        session.commit()
        flash(publisher.name + " deleted")
        return redirect(url_for('all_publishers'))
    else:
        if not publisher.book:
            return render_template('deletePublisher.html', publisher=publisher)
        else:
            return render_template('error.html',
                                   cause='Can\'t delete a publisher with books')

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


@app.route('/recommended/', methods=['GET'])
def get_recommended():
    recommended = session.execute(
        'SELECT * FROM recommended_for_you ORDER BY name').fetchall()
    return render_template("items.html", items=recommended)


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
    on_wishlist = session.query(WishList.WishList).filter_by(customer_id=current_user_id, item_id=item_id).scalar()
    my_rating = session.query(Rating.Rating).filter_by(customer_id=current_user_id, item_id=item_id).scalar()
    num_stars = my_rating.item_rating if my_rating is not None else None
    the_item = session.execute('SELECT * FROM all_items_with_rating WHERE id="' + item_id + '"').fetchone()
    return render_template("item_details.html", item=the_item, on_wishlist=(on_wishlist != None), my_rating=num_stars)


@app.route('/customer/', methods=['GET'])
def get_all_customers():
    all_customers = session.execute("SELECT * FROM all_customers").fetchall()
    return render_template("customers.html", customers=all_customers)


@app.route('/never_bought/', methods=['GET'])
def wish_list_never_bought():
    never_bought = session.execute("SELECT * FROM wish_list_never_purchased").fetchall()
    return render_template("never_bought.html", never_bought=never_bought)

@app.route('/author/', methods=['GET'])
def get_authors():
    authors = get_all_authors()
    return render_template("authors.html", authors=authors)

@app.route('/author/<int:author_id>/')
def one_author(author_id):
    author = session.query(Author.Author).filter_by(author_id=author_id).one()
    return render_template('publisher.html',
                           author=author)


@app.route('/add_author/',methods=['GET','POST'])
def add_author():
    if request.method == 'POST':
        first_name=request.form['author_first_name']
        last_name=request.form['author_last_name']
        author = Author.Author(first_name=first_name,last_name=last_name)
        session.add(author)
        session.commit()
        flash("New author " + first_name + " " + last_name + " created")
        return redirect(url_for('get_authors'))
    else:
        return render_template('newAuthor.html')


@app.route('/author/modify/<int:author_id>', methods=['GET','POST'])
def modify_author(author_id):
    author = session.query(Author.Author).filter_by(author_id=author_id).one()
    if request.method == 'POST':
        author.first_name=request.form['author_first_name']
        author.last_name=request.form['author_last_name']
        session.add(author)
        session.commit()
        flash("Author " + author.first_name + " " + author.last_name + " edited")
        return redirect(url_for('get_authors'))
    else:
        return render_template('editAuthor.html',
                               author=author)


@app.route('/author/delete/<int:author_id>/', methods=['GET', 'POST'])
def delete_author(author_id):
    author = session.query(Author.Author).filter_by(author_id=author_id).one()
    if request.method == 'POST':
        session.delete(author)
        session.commit()
        flash(author.first_name+ " " + author.last_name + " deleted")
        return redirect(url_for('get_authors'))
    else:
        if not author.book:
            return render_template('deleteAuthor.html', author=author)
        else:
            return render_template('error.html',
                                   cause='Can\'t delete an author with books')

@app.route('/cart/', methods=['GET'])
def get_cart():
    cart = session.execute(
        'SELECT i.*, c.quantity FROM cart c JOIN all_items i on i.id = c.item_id WHERE c.customer_id = ' + str(
            current_user_id)).fetchall()
    return render_template("cart.html", cart=cart)



@app.route('/add_to_cart/<string:item_id>', methods=['POST'])
def add_to_cart(item_id):
    quantity = request.form['quantity']

    try:
        cart_item = session.query(Cart.Cart).filter_by(customer_id=current_user_id, item_id=item_id).one()
        cart_item.quantity += int(quantity)
        session.add(cart_item)
    except Exception as e:
        cart_item = Cart.Cart(item_id=item_id, customer_id=current_user_id, quantity=quantity)
        session.add(cart_item)
    session.commit()
    return redirect(url_for('get_cart'))


@app.route('/remove_from_cart/<string:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    try:
        cart_item = session.query(Cart.Cart).filter_by(customer_id=current_user_id, item_id=item_id).one()
        session.delete(cart_item)
        session.commit()
        return redirect(url_for('get_cart'))
    except:
        # Already deleted, don't do anything
        pass
        return redirect(url_for('get_cart'))


@app.route('/wishlist/', methods=['GET'])
def get_wishlist():
    current_user_id = 1
    all_items = session.execute(
        'SELECT i.* FROM wish_list w JOIN all_items i on i.id = w.item_id WHERE w.customer_id = ' + str(current_user_id)).fetchall()
    return render_template("items.html", items=all_items, subtitle = "Wishlist")


@app.route('/add_to_wishlist/<string:item_id>', methods=['POST'])
def add_to_wishlist(item_id):
    try:
        wish_list_item = session.query(WishList.WishList).filter_by(customer_id=current_user_id, item_id=item_id).one()
        # Already on the wishlist, don't do anything
        return redirect(url_for('get_wishlist'))
    except:
        wish_list_item = WishList.WishList(item_id=item_id, customer_id=current_user_id)
        session.add(wish_list_item)
        session.commit()
        return redirect(url_for('get_wishlist'))


@app.route('/remove_from_wishlist/<string:item_id>', methods=['POST'])
def remove_from_wishlist(item_id):
    try:
        wish_list_item = session.query(WishList.WishList).filter_by(customer_id=current_user_id, item_id=item_id).one()
        session.delete(wish_list_item)
        session.commit()
        return redirect(url_for('get_wishlist'))
    except:
        # Already deleted, don't do anything
        pass
        return redirect(url_for('get_wishlist'))


@app.route('/checkout/', methods=['POST'])
def checkout():
    day = session.execute(
        'SELECT day_of_week FROM when_will_order_ship').fetchone()

    current_user_id = 1
    cart = session.query(Cart.Cart).filter_by(customer_id=current_user_id).all()

    for cart_item in cart:
        session.add(Transaction.Transaction(item_id=cart_item.item_id, quantity=cart_item.quantity, customer_id=current_user_id))
        session.delete(cart_item)
    session.commit()

    return "Order successful! Orders bought today will ship on " + day["day_of_week"]\
           + "<br/> <a href = '/'>Buy more stuff!</a>"



@app.route('/rate_item/<string:item_id>', methods=['POST'])
def rate_item(item_id):
    stars = request.form['stars']

    try:
        rating = session.query(Rating.Rating).filter_by(customer_id=current_user_id, item_id=item_id).one()
        rating.item_rating = int(stars)
    except Exception as e:
        rating = Rating.Rating(item_id=item_id, customer_id=current_user_id, item_rating=str(stars))
    session.add(rating)
    session.commit()
    return redirect(url_for('get_specific_item', item_id=item_id))



##helper functions
def get_all_authors():
    authors = session.query(Author.Author).all()
    return authors

def get_all_genres():
    genres = session.query(Genre.Genre).all()
    return genres

def get_all_publishers():
    publisher = session.query(Publisher.Publisher).all()
    return publisher

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()

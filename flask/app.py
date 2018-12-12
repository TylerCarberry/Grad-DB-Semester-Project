import os
import urllib
import time

from flask import Flask, render_template, url_for, request, flash, redirect, Blueprint

#app = Flask(__name__)

page = Blueprint('carberryt9', __name__, static_folder='static', template_folder='templates')

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
password = 'mustardday'
# ON ELVIS
connection = create_engine('mysql://carberryt9:mustardday@localhost/carberryt9', isolation_level='READ_COMMITTED')
# ON LOCAL
# connection = create_engine('mysql+pymysql://'+'username:password'+':@localhost:3306/'+'schemaName')

BASE.metadata.create_all(connection)

# create a session that we can use to interact with the database
Session = sessionmaker(bind=connection)
# create a session for our use from our generated Session class.
session = Session()

current_user_id = 0


@page.route('/')
def home():
    return render_template("./carberryt9/home.html")


@page.route('/shop/')
def shop():
    global current_user_id
    current_user_id = 1
    return "<h1>Shop</h1>" \
           "<p><a href='../recommended'>Recommended for you</a></p>" \
           "<p><a href='../categories'>Shop By Category</a></p>" \
           "<p><a href='../wishlist'>View Wishlist</a></p>" \
           "<p><a href='../cart'>View Your Cart</a></p>"


# TODO: Make this a template
@page.route('/admin/')
def admin():
    global current_user_id
    current_user_id = 0
    return "<h1>Welcome to Rowan Bookstore - Admin Page</h1>" \
           "<p><a href='../low_inventory'> Inventory that has fallen below the minimum stock level</a></p>" \
           "<p><a href='../when_ship'> When will orders ship?</a></p>" \
           "<p><a href='../never_bought'> Wish list but never bought</a></p>" \
           "<p><a href='../not_active_customers'> Not active customers</a></p>" \
           "<p><a href='../most_wished_category'> Most wished for item in each category</a></p>" \
           "<br/>" \
           "<p><a href='../items_sold_day_of_week'>EXTRA CREDIT: Number of items sold per day of week</a></p>" \
           "<p><a href='../customers_spent_most'>EXTRA CREDIT: Customers who spent the most money</a></p>" \
           "<br/>" \
           "<p><a href='../customers/'>View Our Customers</a></p>" \
           "<p><a href='../all_customers/'>View All Customers (Due to a bug, viewing all customers takes a minute to load. The link below excludes adventureworks)</a></p>" \
           "<p><a href='../most_customers/'>View Most Customers</a></p>" \
           "<br/>" \
           "<p><a href='../book'>View All Books</a></p>" \
           "<p><a href='../author'>View All Authors</a></p>" \
           "<p><a href='../publisher'>View All Publishers</a></p>"


@page.route('/low_inventory/')
def low_inventory():
    inventory = session.execute(
        'SELECT title as name, concat("rowan_", book_id) as id FROM low_inventory ORDER BY title').fetchall()
    return render_template("./carberryt9/items.html", items=inventory)


@page.route('/when_ship/')
def when_ship():
    day = session.execute(
        'SELECT day_of_week FROM when_will_order_ship').fetchone()
    return "Orders bought today will ship on " + day["day_of_week"]


@page.route('/not_active_customers/', methods=['GET'])
def not_active_customers():
    all_customers = session.execute("SELECT * FROM not_active_customers").fetchall()
    return render_template("./carberryt9/all_customers.html", customers=all_customers)


@page.route('/items_sold_day_of_week/', methods=['GET'])
def num_sold_day_week():
    num_sold_day_week = session.execute("SELECT * FROM items_sold_day_of_week").fetchall()
    return render_template("./carberryt9/num_sold_day_of_week.html", num_sold_day_week=num_sold_day_week)


@page.route('/customers_spent_most/', methods=['GET'])
def customers_spent_most():
    customers_spent_most = session.execute("SELECT * FROM customers_spent_most").fetchall()
    return render_template("./carberryt9/customers_spent_most.html", customers_spent_most=customers_spent_most)



@page.route('/most_wished_category/', methods=['GET'])
def most_wished_category():
    most_wished_category = session.execute("SELECT * FROM most_wished_for_item_every_category").fetchall()
    return render_template("./carberryt9/most_wished_category.html", most_wished_category=most_wished_category)


@page.route('/book/')
def all_books():
    books = session.query(Book.Book).all()
    return render_template('./carberryt9/booklist.html',
                           books=books,
                           title='All Books')


@page.route('/book/<int:bookId>/')
def one_book(bookId):
    book = session.query(Book.Book).filter_by(book_id=bookId).one()
    return render_template('./carberryt9/book.html',
                           book=book,
                           title=book.title,
                           current_user_id=current_user_id)


@page.route('/book/modify/<int:book_id>/', methods=['GET', 'POST'])
def modify_book(book_id):
    book = session.query(Book.Book).filter_by(book_id=book_id).one()
    if request.method == 'POST':
        book.title = request.form['title']
        book.description = request.form['description']
        book.pages = request.form['pages']
        new_author_id = int(request.form['new_author'])

        for author in book.authors:
            current_author_id = request.form['author_id_' + str(author.author_id)]
            if int(current_author_id) == 0:
                itemToBeDeleted = session.query(Author.Author_Book).filter_by(author_id=author.author_id,
                                                                              book_id=book.book_id).one()
                session.delete(itemToBeDeleted)
            else:
                session.query(Author.Author_Book).filter_by(author_id=author.author_id, book_id=book.book_id).update(
                    {"author_id": current_author_id})

        if new_author_id != 0:
            author = session.query(Author.Author).filter_by(author_id=new_author_id).one()
            book.addAuthor(author)

        for genre in book.genres:
            current_genre_id = request.form['genre_id_' + str(genre.genre_id)]
            if int(current_genre_id) == 0:
                itemToBeDeleted = session.query(Genre.Book_Genre).filter_by(genre_id=genre.genre_id,
                                                                            book_id=book.book_id).one()
                session.delete(itemToBeDeleted)
            else:
                session.query(Genre.Book_Genre).filter_by(genre_id=genre.genre_id, book_id=book.book_id).update(
                    {"genre_id": current_genre_id})

        new_genre_id = int(request.form['new_genre'])

        if new_genre_id != 0:
            genre = session.query(Genre.Genre).filter_by(genre_id=new_genre_id).one()
            book.addGenre(genre)

        book.release_year = request.form['release_year']
        book.price = request.form['price']
        book.num_in_stock = request.form['stock']
        # put this in if things break, also requires change to editBook.html
        pub_id = request.form['publisher_id']
        book.publisher_id = pub_id
        #book.publisher.publisher_id = int(request.form['publisher_id'])
        session.add(book)
        session.commit()
        flash(book.title + "'s information updated")
        return redirect(url_for('all_books'))
    else:
        authors = get_all_authors()
        genres = get_all_genres()
        publishers = get_all_publishers()
        return render_template('./carberryt9/editBook.html', book=book, allAuthors=authors, allGenres=genres,
                               allPublishers=publishers)


@page.route('/book/delete/<int:book_id>/', methods=['GET', 'POST'])
def delete_book(book_id):
    book = session.query(Book.Book).filter_by(book_id=book_id).one()
    if request.method == 'POST':
        deletedAuthorConnections= session.query(Author.Author_Book).filter_by(book_id=book.book_id).all()
        for author in deletedAuthorConnections:
            session.delete(author)
        deletedGenreConnections=session.query(Genre.Book_Genre).filter_by(book_id=book.book_id).all()
        for genre in deletedGenreConnections:
            session.delete(genre)
        session.delete(book)
        session.commit()
        flash(book.title + " deleted")
        return redirect(url_for('all_books'))
    else:
        return render_template('./carberryt9/deleteBook.html', book=book)


@page.route('/book/new/', methods=['GET', 'POST'])
def insert_book():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        num_in_stock = request.form['stock']
        pages = request.form['pages']
        release_year = request.form['release_year']
        price = request.form['price']
        author = session.query(Author.Author).filter_by(author_id=request.form['author_id']).one()
        publisher = session.query(Publisher.Publisher).filter_by(publisher_id=request.form['publisher_id']).one()
        genre = session.query(Genre.Genre).filter_by(genre_id=request.form['genre_id']).one()
        newBook = Book.Book(title=title, description=description, num_in_stock=num_in_stock, pages=pages,
                            release_year=release_year, author=author, price=price, genre=genre, publisher=publisher)
        session.add(newBook)
        session.commit()
        flash("New book " + title + " created")
        return redirect(url_for('all_books'))
    else:
        authors = get_all_authors()
        genres = get_all_genres()
        publishers = get_all_publishers()
        return render_template('./carberryt9/newBook.html', authors=authors, genres=genres, publishers=publishers)


@page.route('/publisher/')
def all_publishers():
    publishers = session.query(Publisher.Publisher).all()
    return render_template('./carberryt9/publisherlist.html',
                           publishers=publishers)


@page.route('/publisher/<int:publisher_id>/')
def one_publisher(publisher_id):
    publisher = session.query(Publisher.Publisher).filter_by(publisher_id=publisher_id).one()
    return render_template('./carberryt9/publisher.html',
                           publisher=publisher)


@page.route('/publisher/new/', methods=['GET', 'POST'])
def new_publisher():
    if request.method == 'POST':
        name = request.form['publisher_name']
        publisher = Publisher.Publisher(name)
        session.add(publisher)
        session.commit()
        flash("New publisher " + name + " created")
        return redirect(url_for('all_publishers'))
    else:
        return render_template('./carberryt9/newPublisher.html')


@page.route('/publisher/modify/<int:publisher_id>', methods=['GET', 'POST'])
def modify_publisher(publisher_id):
    publisher = session.query(Publisher.Publisher).filter_by(publisher_id=publisher_id).one()
    if request.method == 'POST':
        publisher.name = request.form['publisher_name']
        session.add(publisher)
        session.commit()
        flash("Publisher " + publisher.name + " edited")
        return redirect(url_for('all_publishers'))
    else:
        return render_template('./carberryt9/editPublisher.html',
                               publisher=publisher)


@page.route('/publisher/delete/<int:publisher_id>/', methods=['GET', 'POST'])
def delete_publisher(publisher_id):
    publisher = session.query(Publisher.Publisher).filter_by(publisher_id=publisher_id).one()
    if request.method == 'POST':
        session.delete(publisher)
        session.commit()
        flash(publisher.name + " deleted")
        return redirect(url_for('all_publishers'))
    else:
        if not publisher.book:
            return render_template('./carberryt9/deletePublisher.html', publisher=publisher)
        else:
            return render_template('./carberryt9/error.html',
                                   cause='Can\'t delete a publisher with books')


@page.route('/categories/', methods=['GET'])
def get_categories():
    categories = session.execute("SELECT name FROM all_categories ORDER BY name").fetchall()

    converted = []

    for cat in categories:
        it = dict(cat)
        it['encoded_name'] = urllib.parse.quote_plus(it['name'])
        converted.append(it)

    return render_template('./carberryt9/categories.html', categories=converted)


@page.route('/specials/', methods=['GET'])
def get_specials():
    specials = session.execute(
        'SELECT * FROM specials ORDER BY name').fetchall()
    return render_template("./carberryt9/items.html", items=specials)


@page.route('/recommended/', methods=['GET'])
def get_recommended():
    recommended = session.execute(
        'SELECT * FROM recommended_for_you ORDER BY name').fetchall()
    return render_template("./carberryt9/items.html", items=recommended)


@page.route('/item/', methods=['GET'])
def get_all_items():
    category = request.args.get('category')
    if category is not None:
        all_items = session.execute(
            'SELECT * FROM all_items WHERE category LIKE "%' + category + '%" ORDER BY name').fetchall()
    else:
        all_items = session.execute("SELECT * FROM all_items").fetchall()
    return render_template("./carberryt9/items.html", items=all_items)


@page.route('/item/<string:item_id>/', methods=['GET'])
def get_specific_item(item_id):
    on_wishlist = session.query(WishList.WishList).filter_by(customer_id=current_user_id, item_id=item_id).scalar()
    my_rating = session.query(Rating.Rating).filter_by(customer_id=current_user_id, item_id=item_id).scalar()
    num_stars = my_rating.item_rating if my_rating is not None else None
    the_item = session.execute('SELECT * FROM all_items_with_rating WHERE id="' + item_id + '"').fetchone()
    return render_template("./carberryt9/item_details.html", item=the_item, on_wishlist=(on_wishlist != None), my_rating=num_stars)


@page.route('/all_customers/', methods=['GET'])
def get_all_customers():
    print("HELLO!")
    # There is a bug with our database where unioning all 4 stores together takes a really long time
    # Splitting it up in to multiple queries runs much faster
    all_customers = session.execute("SELECT * FROM rowan_customers").fetchall()
    print("ROWAN!")
    all_customers2 = session.execute("SELECT * FROM sakila_customers").fetchall()
    print("SAKILA!")
    all_customers3 = session.execute("SELECT * FROM northwind_customers").fetchall()
    print("NORTH!")
    all_customers4 = session.execute("SELECT * FROM adventure_customers").fetchall()
    print("ADVENTURE!")
    return render_template("./carberryt9/all_customers.html", customers=all_customers, customers2=all_customers2, customers3=all_customers3, customers4=all_customers4)



@page.route('/most_customers/', methods=['GET'])
def get_most_customers():
    print("HELLO!")
    # There is a bug with our database where unioning all 4 stores together takes a really long time
    # Splitting it up in to multiple queries runs much faster
    all_customers = session.execute("SELECT * FROM rowan_customers").fetchall()
    print("ROWAN!")
    all_customers2 = session.execute("SELECT * FROM sakila_customers").fetchall()
    print("SAKILA!")
    all_customers3 = session.execute("SELECT * FROM northwind_customers").fetchall()
    print("NORTH!")
    all_customers4 = [] #session.execute("SELECT * FROM adventure_customers").fetchall()
    print("ADVENTURE!")
    return render_template("./carberryt9/all_customers.html", customers=all_customers, customers2=all_customers2, customers3=all_customers3, customers4=all_customers4)





@page.route('/never_bought/', methods=['GET'])
def wish_list_never_bought():
    never_bought = session.execute("SELECT * FROM wish_list_never_purchased").fetchall()
    return render_template("./carberryt9/never_bought.html", never_bought=never_bought)


@page.route('/author/', methods=['GET'])
def get_authors():
    authors = get_all_authors()
    return render_template("./carberryt9/authors.html", authors=authors)


@page.route('/author/<int:author_id>/')
def one_author(author_id):
    author = session.query(Author.Author).filter_by(author_id=author_id).one()
    return render_template('./carberryt9/author.html',
                           author=author)


@page.route('/add_author/', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        first_name = request.form['author_first_name']
        last_name = request.form['author_last_name']
        author = Author.Author(first_name=first_name, last_name=last_name)
        session.add(author)
        session.commit()
        flash("New author " + first_name + " " + last_name + " created")
        return redirect(url_for('get_authors'))
    else:
        return render_template('./carberryt9/newAuthor.html')


@page.route('/author/modify/<int:author_id>/', methods=['GET', 'POST'])
def modify_author(author_id):
    author = session.query(Author.Author).filter_by(author_id=author_id).one()
    if request.method == 'POST':
        author.first_name = request.form['author_first_name']
        author.last_name = request.form['author_last_name']
        session.add(author)
        session.commit()
        flash("Author " + author.first_name + " " + author.last_name + " edited")
        return redirect(url_for('get_authors'))
    else:
        return render_template('./carberryt9/editAuthor.html',
                               author=author)


@page.route('/author/delete/<int:author_id>/', methods=['GET', 'POST'])
def delete_author(author_id):
    author = session.query(Author.Author).filter_by(author_id=author_id).one()
    if request.method == 'POST':
        session.delete(author)
        session.commit()
        flash(author.first_name + " " + author.last_name + " deleted")
        return redirect(url_for('get_authors'))
    else:
        if not author.books:
            return render_template('./carberryt9/deleteAuthor.html', author=author)
        else:
            return render_template('./carberryt9/error.html',
                                   cause='Can\'t delete an author with books')


@page.route('/cart/', methods=['GET'])
def get_cart():
    cart = session.execute(
        'SELECT i.*, c.quantity FROM cart c JOIN all_items i on i.id = c.item_id WHERE c.customer_id = ' + str(
            current_user_id)).fetchall()
    return render_template("./carberryt9/cart.html", cart=cart)


@page.route('/add_to_cart/<string:item_id>', methods=['POST'])
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


@page.route('/remove_from_cart/<string:item_id>', methods=['POST'])
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


@page.route('/wishlist/', methods=['GET'])
def get_wishlist():
    current_user_id = 1
    all_items = session.execute(
        'SELECT i.* FROM wish_list w JOIN all_items i on i.id = w.item_id WHERE w.customer_id = ' + str(
            current_user_id)).fetchall()
    return render_template("./carberryt9/items.html", items=all_items, subtitle="Wishlist")


@page.route('/add_to_wishlist/<string:item_id>', methods=['POST'])
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


@page.route('/remove_from_wishlist/<string:item_id>', methods=['POST'])
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


@page.route('/checkout/', methods=['POST'])
def checkout():
    day = session.execute(
        'SELECT day_of_week FROM when_will_order_ship').fetchone()

    current_user_id = 1
    cart = session.query(Cart.Cart).filter_by(customer_id=current_user_id).all()

    for cart_item in cart:
        if "rowan_" in cart_item.item_id:
            our_id = cart_item.item_id.replace("rowan_", "")
            book_item = session.query(Book.Book).filter_by(book_id=our_id).one()
            book_item.num_in_stock = cart_item.quantity
            session.add(book_item)
            session.commit()

        session.add(Transaction.Transaction(item_id=cart_item.item_id, quantity=cart_item.quantity,
                                            customer_id=current_user_id))
        session.delete(cart_item)
        session.commit()

    return "Order successful! Orders bought today will ship on " + day["day_of_week"] \
           + "<br/> <a href = '/carberryt9/shop/'>Buy more stuff!</a>"


@page.route('/rate_item/<string:item_id>', methods=['POST'])
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


@page.route('/customers/')
def our_customers():
    customers = session.query(Customer.Customer).all()
    return render_template('./carberryt9/our_customers.html',
                           customers=customers)


@page.route('/customer/<int:customer_id>/')
def one_customer(customer_id):
    customer = session.query(Customer.Customer).filter_by(customer_id=customer_id).one()
    return render_template('./carberryt9/customer.html',
                           customer=customer)


@page.route('/customer/new/', methods=['GET', 'POST'])
def new_customer():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        customer = Customer.Customer(first_name=first_name, last_name=last_name, address=address, email=email)
        session.add(customer)
        session.commit()
        flash("New customer " + first_name + " " + last_name + " created")
        return redirect(url_for('our_customers'))
    else:
        return render_template('./carberryt9/newCustomer.html')


@page.route('/customer/modify/<int:customer_id>', methods=['GET', 'POST'])
def modify_customer(customer_id):
    customer = session.query(Customer.Customer).filter_by(customer_id=customer_id).one()
    if request.method == 'POST':
        customer.first_name = request.form['first_name']
        customer.last_name = request.form['last_name']
        customer.address = request.form['address']
        customer.email = request.form['email']
        session.add(customer)
        session.commit()
        flash("Customer " + customer.first_name + " " + customer.last_name + " edited")
        return redirect(url_for('our_customers'))
    else:
        return render_template('./carberryt9/editCustomer.html',
                               customer=customer)


@page.route('/customer/delete/<int:customer_id>/', methods=['GET', 'POST'])
def delete_customer(customer_id):
    customer = session.query(Customer.Customer).filter_by(customer_id=customer_id).one()
    if request.method == 'POST':
        session.delete(customer)
        commit()
        flash(customer.first_name + " " + customer.last_name + "deleted")
        return redirect(url_for('our_customers'))
    else:
        return render_template('./carberryt9/deleteCustomer.html', customer=customer)


##helper functions
def get_all_authors():
    authors = session.query(Author.Author).all()
    return authors


def get_all_genres():
    genres = session.query(Genre.Genre).order_by('name').all()
    return genres


def get_all_publishers():
    publisher = session.query(Publisher.Publisher).all()
    return publisher


def commit():
    try:
        session.commit()
    except Exception as e:
        session.rollback()


# if __name__ == '__main__':
#     app.secret_key = os.urandom(24)
#     app.run()

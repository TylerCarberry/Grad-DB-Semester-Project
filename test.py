from sqlalchemy import and_, or_, not_
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

# use a constant here, so that the same bases is used for all tables
# Now save this schema information to the database
from EntitiesAsClasses import Author, Customer, Book, Publisher, Rating, Restock, Transaction, WishList, Genre, Cart
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

# Your Rowan username
username = 'carberryt9'

# The password to the database. Not your Rowan password!
password = 'mustardday'
# ON ELVIS
connection = create_engine('mysql+pymysql://' + username + ':' + password + '@elvis.rowan.edu/' + username)
# ON LOCAL
# connection = create_engine('mysql+pymysql://'+'username:password'+':@localhost:3306/'+'schemaName')
BASE.metadata.create_all(connection)

# create a session that we can use to interact with the database
Session = sessionmaker(bind=connection)
# create a session for our use from our generated Session class.
session = Session()

b = Book.Book(title = "hi", description="this is the description", num_in_stock=50, pages=200, release_year=2018, price=19.99)
#Author.Author_Book()
session.add(b)
session.commit()
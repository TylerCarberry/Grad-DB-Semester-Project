'''
Use the orm framework and classes for tables to query sakila.
Created on Jun 2, 2018

@author: jack
'''

from sqlalchemy import and_, or_, not_
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker



# use a constant here, so that the same bases is used for all tables
# Now save this schema information to the database
from EntitiesAsClasses import Author, Customer, Book
from EntitiesAsClasses.Base import BASE

# Your Rowan username
username = 'smithj1'

# The password to the database. Not your Rowan password!
password = 'password123'

connection = create_engine('mysql+pymysql://' + username + ':' + password + '@elvis.rowan.edu/' + username)
BASE.metadata.create_all(connection)

# create a session that we can use to interact with the database
Session = sessionmaker(bind=connection)
# create a session for our use from our generated Session class.
session = Session()

# Let's try to retrieve all records from some tables
# For film table, we will bring back all records into a single variable films
print("Films:\n")
films = session.query(Book.Book).all()
print(films)

"""
# For actor table, we will use an iterable and chain to order_by method
print("\nActors:\n")
for actor in session.query(Actor).order_by(Actor.last_name):
    print(actor)

# Print certain fields from the first actor
print("\nOur first actor:")
print(session.query(Actor.first_name, Actor.last_name).first())

# More advanced queries
print("\nCount of films")
print(session.query(func.count(Film.film_id)).scalar())  # scalar for a single value

print("\nBinge watching all movies will take this many minutes:")
print(session.query(func.sum(Film.length)).scalar())

print("\nFilms not for children: ")
rFilms = session.query(Film).filter(
    or_(
        Film.rating == 'R',
        Film.rating == "NC-17"))
for film in rFilms:
    print("- " + film.title + " is rated " + film.rating)

print("\nJoined query - stars in `Operation` films")
# another way to do method chaining
operationFilms = session.query(Film.title, Actor.first_name, Actor.last_name)
operationFilms = operationFilms.filter(Film.title.like('%Operation%'))
operationFilms = operationFilms.join(Film_Actor).join(Actor)
operationFilms = operationFilms.order_by(Actor.last_name)
# Note that Film is the first table assumed to be in the where clause
for film in operationFilms:
    print("- " + film.first_name + " " + film.last_name + " (" + film.title + ")")

"""


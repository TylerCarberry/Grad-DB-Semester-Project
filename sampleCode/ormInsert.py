'''
Created on Nov 4, 2018

@author: Stanimir
'''
from EntitiesAsClasses.Author import Author, Author_Book
from EntitiesAsClasses.Book import Book
from EntitiesAsClasses.Publisher import Publisher

from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()

from sqlalchemy import create_engine
connection = create_engine('mysql+pymysql://'+'username:password'+':@localhost:3306/'+'schemaName')
BASE.metadata.create_all(connection)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=connection)
session = Session()

#make a publisher
publisher_name = 'Bloomsbury Publishing'

publisher = Publisher(publisher_name)

author_name_first = 'Joanne'
author_name_last = 'Rowling'

author = Author(author_name_first,author_name_last)
session.add(publisher)
session.add(author)
session.commit()

book_title = 'Harry Potter and the Philosopher\'s Stone'
num_in_stock = 47
pages = 223
release_year = 1997


book = Book(book_title,num_in_stock,pages,release_year,author.author_id)

session.add(book)
session.commit()

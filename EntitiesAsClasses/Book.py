'''
Created on Nov 3, 2018

@author: Stanimir
'''

from sqlalchemy import Column, String, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, DOUBLE
from sqlalchemy.orm import relationship, backref

from EntitiesAsClasses import Author
from EntitiesAsClasses.Base import BASE
from sqlalchemy.sql.schema import ForeignKeyConstraint


class Book(BASE):
    __tablename__ = 'book'

    book_id = Column(INTEGER(unsigned=True), nullable=False, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    num_in_stock = Column(INTEGER(unsigned=True), nullable=False)
    pages = Column(INTEGER(unsigned=True), nullable=False)
    release_year = Column(INTEGER(unsigned=True), nullable=True)
    publisher_id = Column(INTEGER(unsigned=True), ForeignKey('publisher.publisher_id'), nullable=False)
    price = Column(DOUBLE, nullable=False)

    publisher = relationship("Publisher", backref=backref('book'))
    authors = relationship("Author", secondary='author_book', viewonly=True)
    # genres = relationship("Genre", secondary='book_genre', viewonly=True)

    __table_args__ = (
        PrimaryKeyConstraint('book_id', name='PRIMARY'),
        ForeignKeyConstraint(['publisher_id'], ['publisher.publisher_id']))

    def __init__(self, title, description, num_in_stock, pages, release_year, author, price):
        self.title = title
        self.description = description
        self.num_in_stock = num_in_stock
        self.pages = pages
        self.release_year = release_year
        self.price = price
        self.addAuthor(author)

    def addAuthor(self, author):
        newEntry = Author.Author_Book(author=author, book=self)
        self.author_book.append(newEntry)

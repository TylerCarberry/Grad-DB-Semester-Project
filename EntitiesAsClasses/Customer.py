'''
Created on Nov 3, 2018

@author: Jatin Bhakta
'''

from sqlalchemy import Column, String, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey, ForeignKeyConstraint

from EntitiesAsClasses.Base import BASE


class Customer(BASE):
    __tablename__ = 'customer'

    customer_id = Column(INTEGER(unsigned=True), nullable=False, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    address = Column(String(100), nullable=True)

    # wishlist relationship
    books = relationship("Book", secondary="customer_book", viewonly=True)

    # cart relationship
    booksInCart = relationship("Book", secondary="customer_book", viewonly=True)

    __table_args__ = (
        PrimaryKeyConstraint('customer_id', name='PRIMARY'), )

    def __init__(self, first_name, last_name, address):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address


class Customer_Book(BASE):
    __tablename__ = 'customer_book'
    customer_id = Column(INTEGER, ForeignKey('customer.customer_id'), nullable=False)
    book_id = Column(INTEGER, ForeignKey('book.book_id'), nullable=False)

    customer = relationship("Customer", backref=backref("customer_book"))
    book = relationship("Book", backref=backref('customer_book'))

    __table_args__ = (
        PrimaryKeyConstraint('customer_id', 'book_id', name='PRIMARY'),
        ForeignKeyConstraint(['customer_id'], ['customer.customer_id']),
        ForeignKeyConstraint(['book_id'], ['book.book_id']))

    def __init__(self, customer=None, book=None):
        self.customer = customer
        self.book = book
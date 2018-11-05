'''
Created on Nov 3, 2018

@author: Stanimir
'''

from sqlalchemy import Column, String, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship, backref

from EntitiesAsClasses.Base import BASE
from sqlalchemy.sql.schema import ForeignKeyConstraint


class Book(BASE):
    __tablename__ = 'book'

    book_id = Column(INTEGER(unsigned=True), nullable=False, primary_key=True)
    title = Column(String(50), nullable=False)
    num_in_stock = Column(INTEGER(unsigned=True), nullable=False)
    pages = Column(INTEGER(unsigned=True), nullable=False)
    release_year = Column(INTEGER(unsigned=True), nullable=True)
    publisher_id = Column(INTEGER(unsigned=True), nullable=False)

    publisher = relationship("Publisher", backref=backref('publisher'))
    authors = relationship("Author", secondary='author_book',viewonly=True)

    __table_args__ = (
        PrimaryKeyConstraint('book_id', name='PRIMARY'),
        ForeignKeyConstraint(['publisher_id'],['publisher.publisher_id']))

    def __init__(self, title, num_in_stock, pages, release_year, publisher_id, author_id):
        self.title = title
        self.num_in_stock = num_in_stock
        self.pages = pages
        self.release_year = release_year
        self.publisher_id = publisher_id
        self.author_id = author_id

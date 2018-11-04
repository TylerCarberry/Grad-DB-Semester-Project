'''
Created on Nov 3, 2018

@author: Stanimir
'''

from sqlalchemy import Column, String, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.orm import relationship, backref
from EntitiesAsClasses.base import BASE

class Book(BASE):
    __tablename__ = 'book'
    
    book_id = Column(SMALLINT(unsigned=True), nullable=False, primary_key=True)
    title = Column(String(50),nullable=False)
    num_in_stock = Column(SMALLINT(unsigned=True), nullable=False)
    pages = Column(SMALLINT(unsigned=True),nullable=False)
    release_year = Column(SMALLINT(unsigned=True),nullable=True)

    publisher = relationship("Publisher",viewonly=True)
    author = relationship("Author", backref=backref('author'))
    genres = relationship("Genre",viewonly=True)
    
    
    __table_args__ =(
        PrimaryKeyConstraint('book_id',name='PRIMARY'))

    def __init__(self, title,num_in_stock,pages,release_year,publisher_id,author_id):
        self.title = title
        self.num_in_stock = num_in_stock
        self.pages = pages
        self.release_year = release_year
        self.publisher_id = publisher_id
        self.author_id = author_id
    

        
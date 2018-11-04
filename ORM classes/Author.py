'''
Created on Nov 3, 2018

@author: Stanimir
'''

from sqlalchemy import Column, String, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.orm import relationship, backref

from EntitiesAsClasses.base import BASE
from sqlalchemy.sql.schema import ForeignKey, ForeignKeyConstraint

class Author(BASE):
    __tablename__ = 'author'
    
    author_id = Column(SMALLINT(unsigned=True), nullable=False, primary_key=True)
    first_name = Column(String(50),nullable=False)
    last_name = Column(String(50),nullable=False)
    
    books = relationship("Book",secondary="Author_Book", viewOnly=True)
    
    __table_args__ =(
        PrimaryKeyConstraint('author_id',name='PRIMARY'))

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        
class Author_Book(BASE):
    __tablename__ = 'author_book'
    author_id = Column(SMALLINT, ForeignKey('author.author_id'),nullable=False)
    book_id = Column(SMALLINT, ForeignKey('book.book_id'),nullable=False)
    
    author = relationship("Author",backref=backref("author_book"))
    book = relationship("Book",backref=backref('author_book'))
    
    __table_args__ = (
        PrimaryKeyConstraint('author_id','book_id', name='PRIMARY'),
        ForeignKeyConstraint(['author_id'],['author.author_id']),
        ForeignKeyConstraint(['book_id'],['book.book_id']))

    def __init__(self,author=None,book=None):
        self.author=author
        self.book=book
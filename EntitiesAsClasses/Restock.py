'''
Created on Nov 3, 2018

@author: Jatin Bhakta
'''

from sqlalchemy import Column, String, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey, ForeignKeyConstraint

from EntitiesAsClasses.Base import BASE

# one Book can have many Restock orders
class Restock(BASE):
    __tablename__ = 'restock'

    restock_id = Column(INTEGER(unsigned=True), nullable=False, primary_key=True)
    amount = Column(INTEGER(unsigned=True), nullable=False)
    book_id = Column(INTEGER(unsigned=True), ForeignKey('book.book_id'), nullable=False)

    book = relationship("Book", backref=backref('restock'))

    __table_args__ = (
        PrimaryKeyConstraint('restock_id', name='PRIMARY'), )

    #   Note: Different from the flack constructor, as we will pass book not book_ids
    def __init__(self, amount, book=None):
        self.amount = amount
        self.book = book

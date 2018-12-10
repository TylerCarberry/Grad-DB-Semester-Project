'''
Created on Nov 3, 2018

@author: Stanimir
'''

from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.types import Enum

from EntitiesAsClasses.Base import BASE


class Rating(BASE):
    __tablename__ = 'rating'
    item_rating = Column(INTEGER(unsigned=True),nullable=False)
    item_id = Column(INTEGER(unsigned=True),nullable=False)
    customer_id = Column(INTEGER(unsigned=True),nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('item_id','customer_id',name='PRIMARY'), )

    def __init__(self, item_id, customer_id, item_rating):
        self.item_id = item_id
        self.customer_id = customer_id
        self.item_rating = item_rating


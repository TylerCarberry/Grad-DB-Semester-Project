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
    product_rating = Column(Enum('1','2','3','4','5', name='product_ratings'))
    product_id = Column(INTEGER(unsigned=True),nullable=False)
    customer_id = Column(INTEGER(unsigned=True),nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('product_id','customer_id',name='PRIMARY'), )

    def __init__(self, product_id,customer_id):
        self.product_id = product_id
        self.customer_id = customer_id


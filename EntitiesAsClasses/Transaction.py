'''
Created on Nov 3, 2018

@author: Jatin Bhakta
'''

from datetime import datetime
from sqlalchemy import Column, String, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import ForeignKey, ForeignKeyConstraint

from EntitiesAsClasses.Base import BASE

# one Customer can have many Transactions
class Transaction(BASE):
    __tablename__ = 'transaction'

    transaction_id = Column(INTEGER(unsigned=True), nullable=False, primary_key=True)
    transaction_time = Column(TIMESTAMP, default=datetime.now(), nullable=False)

    customer_id = Column(INTEGER(unsigned=True), ForeignKey('customer.customer_id'), nullable=False)

    customer = relationship("Customer", backref=backref('transaction'))

    __table_args__ = (
        PrimaryKeyConstraint('transaction_id', name='PRIMARY'), )

    #   Note: Different from the flack constructor, as we will pass customer not customer_ids
    def __init__(self, transaction_time, customer=None):
        self.transaction_time = transaction_time
        self.customer = customer

from datetime import datetime

from sqlalchemy import Column, String, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, DOUBLE, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from EntitiesAsClasses.Base import BASE
from sqlalchemy.sql.schema import ForeignKeyConstraint


class Transaction(BASE):
    __tablename__ = 'transaction'

    transaction_time = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    item_id = Column(String(100), nullable=False)
    customer_id = Column(INTEGER, nullable=False)
    quantity = Column(INTEGER(unsigned=True), nullable=False)

    customer = relationship("Customer", backref=backref('transaction'))

    __table_args__ = (
        PrimaryKeyConstraint('transaction_time', 'item_id', 'customer_id', name='PRIMARY'),
        ForeignKeyConstraint(['customer_id'],['customer.customer_id']))

    def __init__(self, item_id, customer_id, quantity):
        #self.transaction_time = transaction_time
        self.item_id = item_id
        self.customer_id = customer_id
        self.quantity = quantity

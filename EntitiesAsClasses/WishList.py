from sqlalchemy import Column, String, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, DOUBLE
from sqlalchemy.orm import relationship, backref

from EntitiesAsClasses.Base import BASE
from sqlalchemy.sql.schema import ForeignKeyConstraint


class WishList(BASE):
    __tablename__ = 'wish_list'

    item_id = Column(INTEGER, nullable=False)
    customer_id = Column(INTEGER, nullable=False)
    seller = Column(String(100), nullable=False)

    customer = relationship("Customer", backref=backref('wish_list'))

    __table_args__ = (
        PrimaryKeyConstraint('item_id', 'customer_id', 'seller', name='PRIMARY'),
        ForeignKeyConstraint(['customer_id'],['customer.customer_id']))

    def __init__(self, item_id, customer_id, seller):
        self.item_id = item_id
        self.customer_id = customer_id
        self.seller = seller

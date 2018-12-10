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
	email = Column(String(100), nullable=False)
	
    __table_args__ = (
        PrimaryKeyConstraint('customer_id', name='PRIMARY'), )

    def __init__(self, first_name, last_name, address, email):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
		self.email = email

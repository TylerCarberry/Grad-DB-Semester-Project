'''
Created on Nov 3, 2018

@author: Stanimir
'''

from sqlalchemy import Column, String, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.orm import relationship, backref

from EntitiesAsClasses.base import BASE


class Publisher(BASE):
    __tablename__ = 'publisher'
    
    publisher_id = Column(SMALLINT(unsigned=True), nullable=False, primary_key=True)
    name = Column(String(50),nullable=False)
    
    book = relationship("Book",backref=backref('publisher'))
    
    __table_args__ =(
        PrimaryKeyConstraint('publisher_id',name='PRIMARY'))

    def __init__(self, name):
        self.name = name
        
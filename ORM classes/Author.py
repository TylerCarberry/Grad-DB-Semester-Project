'''
Created on Nov 3, 2018

@author: Stanimir
'''

from datetime import datetime
from sqlalchemy import Column, String, PrimaryKeyConstraint,Index
from sqlalchemy.dialects.mysql import SMALLINT, TIMESTAMP
from sqlalchemy.orm import relationship

from EntitiesAsClasses.base import BASE

class Author(BASE):
    __tablename__ = 'author'
    
    author_id = Column(SMALLINT(unsigned=True), nullable=False, primary_key=True)
    first_name = Column(String(50),nullable=False)
    last_name = Column(String(50),nullable=False)
    
    __table_args__ =(
        PrimaryKeyConstraint('author_id',name='PRIMARY'))

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
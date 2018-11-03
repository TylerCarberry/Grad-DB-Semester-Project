'''
Created on Nov 3, 2018

@author: Stanimir
'''

from sqlalchemy import Column, String, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.orm import relationship
from EntitiesAsClasses.base import BASE

class Genre(BASE):
    __tablename__ = 'genre'
    
    genre_id = Column(SMALLINT(unsigned=True), nullable=False, primary_key=True)
    name = Column(String(50),nullable=False)
    
    __table_args__ =(
        PrimaryKeyConstraint('genre_id',name='PRIMARY'))

    def __init__(self, name):
        self.name = name
        
        
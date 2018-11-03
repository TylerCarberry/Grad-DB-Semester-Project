'''
Created on Jun 2, 2018

@author: jack

This module creates a declarative base constant that can be shared by other class modules
'''
from sqlalchemy.ext.declarative import declarative_base

BASE = declarative_base()
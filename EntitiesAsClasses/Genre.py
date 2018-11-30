from sqlalchemy import Column, String, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, DOUBLE
from sqlalchemy.orm import relationship, backref

from EntitiesAsClasses.Base import BASE
from sqlalchemy.sql.schema import ForeignKeyConstraint


class Genre(BASE):
    __tablename__ = 'genre'

    genre_id = Column(INTEGER(unsigned=True), nullable=False, primary_key=True)
    name = Column(String(100), nullable=False)

    books = relationship("Book", secondary='book_genre', viewonly=True)

    __table_args__ = (
        PrimaryKeyConstraint('genre_id', name='PRIMARY'),)

    def __init__(self, name):
        self.name = name


class Book_Genre(BASE):
    __tablename__ = 'book_genre'
    book_id = Column(INTEGER, ForeignKey('book.book_id'), nullable=False)
    genre_id = Column(INTEGER, ForeignKey('genre.genre_id'), nullable=False)

    book = relationship("Book", backref=backref("book_genre"))
    genre = relationship("Genre", backref=backref("book_genre"))

    __table_args__ = (
    PrimaryKeyConstraint('book_id', 'genre_id', name='PRIMARY'),
    ForeignKeyConstraint(['book_id'], ['book.book_id']),
    ForeignKeyConstraint(['genre_id'], ['genre.genre_id']))

    def __init__(self, book=None, genre=None):
        self.book = book
        self.genre = genre

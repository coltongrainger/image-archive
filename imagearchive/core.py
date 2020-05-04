#! /usr/bin/env python3
#
# 2020-04-20 
# Colton Grainger 
# CC-0 Public Domain

"""
Prototypical Image Archive
"""


##

# adapted from Essential SQLAlchemy, 2e by Jason Myers and Rick Copeland
# https://github.com/oreillymedia/essential-sqlalchemy-2e/

from sqlalchemy import Table, Column, Integer, String, Date, DateTime
from sqlalchemy import UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.types import Enum

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

from datetime import datetime

# create an instance of the declarative_base
Base = declarative_base()

# inherit from the Base
class Author(Base):

    """Abstraction for authors of documents"""

    # define the table name
    __tablename__ = 'author'

    # add keys, constraints, and indexes
    __table_args__ = \
            (UniqueConstraint('name', 'organization',
                name='uix_author_name_and_organization'),)

    # define an attribute and set it to be a primary key
    author_id = Column(Integer(), primary_key=True)

    # add further attributes (metadata)
    name = Column(String(255))
    email = Column(String(255))
    organization = Column(String(255))

    def __repr__(self):
        return f"Author(name='{self.name}', email='{self.email}', "\
                + f"organization='{self.organization}')"

class Document(Base):

    """Abstraction for documents as linearly ordered collections of images"""

    __tablename__ = 'document'
    __table_args__ = \
            (ForeignKeyConstraint(['author_id'], ['author.author_id']),)

    document_id = Column(Integer(), primary_key=True)

    start_date = Column(Date())
    end_date = Column(Date())
    accession_datetime = Column(DateTime(), default=datetime.now)
    license = Column(String(55), default='CC-0 Public Domain')

    # add related tables and objects
    author_id = Column(Integer(), ForeignKey('author.author_id'))

    # add a relationship directive to provide a property that can be used to
    # access the document's author (this establishes a one-to-many relationship)
    author = relationship('Author', backref=backref('documents', order_by=start_date))

    def __repr__(self):
        return f"Document(author_id='{self.author_id}', "\
                + f"start_date='{self.start_date}', "\
                + f"end_date='{self.end_date}', "\
                + f"accession_datetime='{self.accession_datetime}', "\
                + f"license='{self.license}')"

class Image(Base):

    """Abstraction for images and binary image file metadata"""

    __tablename__ = 'image'
    __table_args__ = \
            (ForeignKeyConstraint(['document_id'], ['document.document_id']),)

    uuid = Column(String(36), primary_key=True)

    # add file-level metadata attributes
    file_size = Column(Integer())                       # number of bytes
    file_media_type = Column(String(10))                # e.g., 'image/tiff'
    file_creation_datetime = Column(DateTime())
    file_modification_datetime = Column(DateTime())
    file_original_name = Column(String(255))

    document_id = Column(Integer(), ForeignKey('document.document_id'))
    # this establishes a one-to-many relationship to access the image's document
    document = relationship("Document", 
            backref=backref('images', order_by=uuid))

    def __repr__(self):
        return f"Image(uuid='{self.uuid}', document_id='{self.document_id}', "\
            + f"file_size='{self.file_size}', "\
            + f"file_media_type='{self.file_media_type}', "\
            + f"file_creation_datetime='{self.file_creation_datetime}', "\
            + f"file_modification_datetime='{self.file_modification_datetime}', "\
            + f"file_original_name='{self.file_original_name}')"

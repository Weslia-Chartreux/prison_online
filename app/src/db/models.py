import uuid

import sqlalchemy
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text, Integer
from sqlalchemy.orm import relationship
import sqlalchemy.ext.declarative as dec


Base = dec.declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    messages_group = relationship("Message_group", back_populates='users')


class Group(Base):
    __tablename__ = 'groups'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String, nullable=False, unique=True)
    type_group = Column(String, nullable=False)
    title = Column(String, nullable=False)
    messages_group = relationship("Message_group", back_populates='groups')


class Message_group(Base):
    __tablename__ = 'messages_group'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = Column(String, nullable=False)
    user_id = Column(sqlalchemy.Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), index=True)
    group_id = Column(sqlalchemy.Integer, ForeignKey(
        'groups.id', ondelete='CASCADE'), index=True)
    text = Column(String, nullable=False)

    users = relationship('User', back_populates='messages_group')
    groups = relationship('Group', back_populates='messages_group')

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 11:10:19 2016

@author: shidephen
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import CONNECTION_STRING

Base = declarative_base()


class MusicInfo(Base):
    """
    歌曲信息
    """
    __tablename__ = 'info'

    music_id    = Column('id', Integer, primary_key=True, autoincrement=True)
    name        = Column(String(100))
    time        = Column(Float)
    style       = Column(String(100))
    bpm         = Column(Integer)
    key         = Column(Integer)
    music_path  = Column(String(255))
    beat_path   = Column(String(255))
    info_path   = Column(String(255))
    chord_path  = Column(String(255))
    type        = Column(Integer)
    avaliable   = Column(Integer)


class ClipInfo(Base):
    """
    片段信息
    """
    __tablename__ = 'clips'

    clip_id     = Column('id', Integer, primary_key=True, autoincrement=True)
    key         = Column(Integer)
    bpm         = Column(Integer)
    path        = Column(String(255))


class ClipMatchMat(Base):
    """
    片段与歌曲匹配数据
    """
    __tablename__ = 'match_matrices'

    matrix_id           = Column('id', Integer, primary_key=True, autoincrement=True)
    music_id            = Column(Integer, ForeignKey('info.id'))
    clip_matrix_path    = Column(String(255))
    score_matrix_path   = Column(Float)


__engine = create_engine(CONNECTION_STRING)
Session = sessionmaker(bind=__engine)

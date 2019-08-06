# coding: utf-8


from sqlalchemy import Column, DECIMAL, Enum, ForeignKey, Index, JSON, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, ENUM, INTEGER, LONGTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MakerOrder(Base):
    __tablename__ = 'maker_order'

    id = Column(BIGINT(12), primary_key=True)
    book_no = Column(String(64, u'utf8mb4_bin'), nullable=False, comment=u'????')
    user_id = Column(BIGINT(12), nullable=False, comment=u'????id')
    hold_currency = Column(String(10, u'utf8mb4_bin'), nullable=False, comment=u'??')
    exchange_currency = Column(String(10, u'utf8mb4_bin'), nullable=False, comment=u'????')
    hold_amount = Column(INTEGER(11), nullable=False, comment=u'????')
    exchange_amount = Column(INTEGER(11), nullable=False, comment=u'????')
    exchange_rate = Column(DECIMAL(10, 3), nullable=False, comment=u'??')
    create_time = Column(INTEGER(11), nullable=False, comment=u'????')
    status = Column(ENUM(u' pending', u'matched', u'canceled', u'sended', u'received', u'set_wallet', u'payed', u'disputed', u'complete'), nullable=False, server_default=text("'sended'"), comment=u'????')

class TakerOrder(Base):
    __tablename__ = 'taker_order'

    id = Column(BIGINT(12), primary_key=True)
    hold_currency = Column(String(10, u'utf8mb4_bin'), nullable=False, comment=u'??')
    exchange_currency = Column(String(10, u'utf8mb4_bin'), nullable=False, comment=u'????')
    hold_amount = Column(INTEGER(11), nullable=False, comment=u'????')
    exchange_amount = Column(INTEGER(11), nullable=False, comment=u'????')
    exchange_rate = Column(DECIMAL(10, 3), nullable=False, comment=u'??')
    user_id = Column(BIGINT(12), nullable=False, comment=u'????id')
    create_time = Column(INTEGER(11), nullable=False, comment=u'????')
    status = Column(ENUM(u'canceled', u'matched', u'sended', u'received', u'set_wallet', u'payed', u'disputed', u'complete'), nullable=False, comment=u'????')
    book_no = Column(String(64, u'utf8mb4_bin'), nullable=False, comment=u'????')
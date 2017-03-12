from sqlalchemy import exists
from stockwalk.models.symbol import Symbol
from stockwalk.models import dbsession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, \
        String, ForeignKey, Float

Base = declarative_base()


class Quote(Base):
    __tablename__ = 'stockwalk_quotes'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), index=True)
    open = Column(Float)
    low = Column(Float)
    high = Column(Float)
    close = Column(Float)
    adj_close = Column(Float)
    symbol_id = Column(Integer, ForeignKey(Symbol.id), nullable=False)
    volume = Column(Integer)
    # section_name = Column(Integer, ForeignKey(ListingSection.id), nullable=True)

    def __repr__(self):
        return "<Quote(date='%s', open='%s', low='%s', high='%s', close='%s', adj_close='%s', symbol='%s', volume='%s')>" % (
                 self.date,
                 self.open,
                 self.low,
                 self.high,
                 self.close,
                 self.adj_close,
                 self.symbol_id,
                 self.volume
                )


    @staticmethod
    def exists(date, symbol):
        """
        Return True if event with datetime_accessed exists and False otherwise
        """
        symbol_id = dbsession.query(Symbol).filter(Symbol.name == symbol).first().id
        (ret, ), = dbsession.query(exists().where(Quote.date == date).where(Quote.symbol_id == symbol_id))
        return ret

    @property
    def serialize(self):
       """
       Return object data in easily serializable format
       """
       return {
           'date': self.date,
           'open': self.open,
           'low': self.low,
           'high': self.high,
           'close': self.close,
           'adj_close': self.adj_close,
           'symbol': self.symbol,
           'volume': self.volume,
       }
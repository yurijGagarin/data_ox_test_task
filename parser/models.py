from sqlalchemy import (
    Column,
    String,
    BigInteger, Date, )
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Listings(Base):
    __tablename__ = "listings"

    data_listing_id = Column(BigInteger, primary_key=True)
    img_url = Column(String)
    title = Column(String)
    date_posted_str = Column(String)
    date_posted_date = Column(Date)
    location = Column(String)
    bedrooms = Column(String)
    description = Column(String)
    price = Column(String)
    currency = Column(String)

    def __repr__(self):
        return "<Listing(id='%s', title='%s')>" % (
            self.id,
            self.title,
        )

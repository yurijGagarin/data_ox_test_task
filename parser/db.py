import os
from datetime import date

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import parser.models

load_dotenv()


engine = create_engine(os.environ["DB_URI"])
Session = sessionmaker(engine, expire_on_commit=False, class_=Session)


def is_listing_exist(listing_id: int) -> bool:
    with Session() as session:
        listing = session.get(parser.models.Listings, listing_id)
        if listing:
            return True
        return False


def create_listing(data_listing_id: int,
                   img_url: str,
                   title: str,
                   date_posted_str: str,
                   date_posted_date: date,
                   location: str,
                   bedrooms: str,
                   description: str,
                   price: str,
                   currency: str):
    with Session() as session:
        current_listing = models.Listings(
            data_listing_id=data_listing_id,
            img_url=img_url,
            title=title,
            date_posted_str=date_posted_str,
            date_posted_date=date_posted_date,
            location=location,
            bedrooms=bedrooms,
            description=description,
            price=price,
            currency=currency,

        )
        session.add(current_listing)
        session.commit()

import math
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, date, timedelta

import httpx
from bs4 import BeautifulSoup
from loguru import logger
from random_user_agent.user_agent import UserAgent

import parser.models
from parser.db import is_listing_exist, Session
from parser.transport import RetryTransport

STARTING_URL = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273'

transport = RetryTransport(httpx.HTTPTransport(retries=20))
user_agent = UserAgent()
headers = {
    "user-agent": user_agent.get_random_user_agent()
}


def get_soup_from_url(url: str = STARTING_URL):
    with httpx.Client(transport=transport, timeout=None, headers=headers) as client:
        r = client.get(url, follow_redirects=True)
    logger.info(f'I`m going to: {url} Status code:{r.status_code}')

    html = r.content
    return BeautifulSoup(
        html,
        'html.parser')


def get_total_pages():
    soup = get_soup_from_url()
    span = soup.find(class_=re.compile("resultsShowingCount"))
    total_pages = 1
    if span:
        total_estate_objects = span.text.strip().split()[-2]
        total_pages = math.ceil(int(total_estate_objects) / 40)

    return total_pages


def parse_all_data():
    logger.info("Start parsing...")
    pages = get_total_pages()
    logger.info(f"We have found {pages} pages to parse")
    urls = [
        f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{i + 1}/c37l1700273' for i in range(pages)
    ]

    with ThreadPoolExecutor() as executor:
        executor.map(parse_page, urls)

    logger.info("Congratulation all data parsed successfully")


def convert_relative_date_to_absolute(date_posted_atr: str):
    today = datetime.now()
    parts = date_posted_atr.strip().split()
    time_delta_val = int(parts[1])
    time_delta_atr = parts[2]
    date_posted = today - timedelta(**{
        time_delta_atr: time_delta_val,
    })

    return date_posted.date()


def get_date_posted(date_posted_atr: str) -> date:
    if '/' in date_posted_atr:
        return datetime.strptime(date_posted_atr, '%d/%m/%Y')
    return convert_relative_date_to_absolute(date_posted_atr)


def get_listing_metadata(ad, data_listing_id_atr):
    img_url_atr = ad.find('img').get('data-src') or "No photo"
    name_atr = ad.find(class_="title").text.strip()
    date_posted_atr = ad.find(class_="date-posted").text
    price_atr = ad.find(class_="price").text.strip()
    location_atr = ad.find(class_="location").find('span').text.strip()
    bedrooms_atr = " ".join(ad.find(class_="bedrooms").text.split())
    description_atr = " ".join(ad.find(class_="description").text.split())
    currency_atr = ad.find(class_="price").text.strip()[0]
    date_posted = get_date_posted(date_posted_atr)
    has_price = '.' in price_atr

    return {
        'data_listing_id': data_listing_id_atr,
        'img_url': img_url_atr,
        'title': name_atr,
        'date_posted_str': datetime.strftime(date_posted, '%d-%m-%Y'),
        'date_posted_date': date_posted,
        'location': location_atr,
        'bedrooms': bedrooms_atr,
        'description': description_atr,
        'price': price_atr[1::] if has_price else price_atr,
        'currency': currency_atr if has_price else "No currency provided"
    }


def parse_page(url):
    soup = get_soup_from_url(url)

    with Session() as session:
        for el in soup.find_all("div", class_=re.compile("search-item")):
            data_listing_id_atr = el["data-listing-id"]
            if is_listing_exist(data_listing_id_atr):
                continue
            metadata = get_listing_metadata(el, data_listing_id_atr)
            current_listing = parser.models.Listings(**metadata)
            session.add(current_listing)

        session.commit()
        logger.info('Record to DB created')


@logger.catch
def main():
    parse_all_data()


if __name__ == "__main__":
    main()

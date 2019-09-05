import re

from bs4 import BeautifulSoup
from urllib import request


def spider(news_topic='default', limit=5):
    """Scrapes landing page of ST.com and several of its main pages.

    Args:
        news_topic (str): news topic to scrape for. Defaults to 'default'.
        limit (int): number of news stories to return per news topic. Defaults to 5.

    Returns:
        List of headlines and urls, depending on the topic passed.
    """
    main_topics = {'singapore', 'asia', 'world', 'politics',
                   'lifestyle', 'business', 'sport'}

    # topics under the singapore category
    singapore = {'transport', 'education', 'housing', 'health',
                 'manpower', 'courts-crime', 'environment'}

    url = 'https://www.straitstimes.com/'
    if news_topic == 'default':             # scrapes landing page
        pass
    elif news_topic in main_topics:         # scrapes main topic page
        url += f'{news_topic.lower()}'
    elif news_topic in singapore:           # scrapes topic page
        url += f'singapore/{news_topic.lower()}'
    else:                                   # scrapes tags page for topic
        url += f'tags/{news_topic.lower()}'

    soup = get_soup(url)
    hrefs = soup.find_all('span', class_='story-headline', limit=limit)

    pattern = 'href=\"(\S*)\">(.*)</a>'
    # pattern: href="(url)">(headline)</a>

    results = list()
    links = re.findall(pattern, str(hrefs))
    for count, (url, headline) in enumerate(links, start=1):
        results.append(
            (count, headline, 'https://www.straitstimes.com' + url)
            )

    return results


def get_h1_text(url):
    """Returns news headline from news article."""
    soup = get_soup(url)
    headline = soup.find('h1', class_='headline node-title').get_text()

    return headline


def get_soup(url):
    """Return BeautifulSoup object from url"""
    html = request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    return soup

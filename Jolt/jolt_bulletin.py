"""
Builds the news bulletin by scraping for stories on ST.com and storing the data in text files.
"""
import json

from jolt_spider import spider


def news_bulletin(user_id):
    """Scrapes news and writes bulletin to user config file.

    Args:
        user_id (int): user id.
    """
    json_file = f'{user_id}_config.json'

    # find topics to scrape from user settings
    topics_to_scrape = list()
    with open(json_file, 'r') as f:
        data = json.load(f)
        topics = data['topics']
        for topic, value in topics.items():
            if value is True:
                topics_to_scrape.append(topic)

    # scrape bulletin info - i.e. headlines and urls
    topics_to_db = dict()
    for topic in topics_to_scrape:
        news = spider(topic)
        topics_to_db[topic] = news

    # update user database with scraped news
    with open(json_file, 'r') as f:
        data = json.load(f)
        data['bulletin'] = topics_to_db
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)

    return


def missed_news(user_id):
    """Checks for any missing piece of news in bulletin.

    Args:
        user_id (int): user id.

    Returns:
        False if all news is in bulletin, True otherwise.
    """
    state = False

    json_file = f'{user_id}_config.json'
    with open(json_file, 'r') as f:
        data = json.load(f)

        bulletin = data['bulletin']
        for topic, stories in bulletin.items():
            if len(stories) == 0:
                state = True
                break

    return state

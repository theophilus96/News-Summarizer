from newspaper import Article


def summarised_article(url):
    """News summariser.

    Args:
        url (str): url of news article to be summarised.

    Returns:
        Title, authors, date, pic, and summary of a news article.
    """
    a = Article(url, language='en')
    a.download()
    a.parse()
    a.nlp()
    title = a.title
    authors = get_byline(a.authors)
    date = pub_date(a.publish_date)
    summary = pretty_summary(a.summary)

    return (title, authors, date, summary)


def get_news_pic(url):
    """Returns url of news header image from news article's url.

    Args:
        url (str): url of news article.

    Returns:
        url of news article's top image.

    """
    a = Article(url, language='en')
    a. download()
    a. parse()

    return a.top_image


def pretty_summary(text):
    """Formats paragraphs of news story.

    Args:
        text (str): news text.

    Returns:
        News article in paragraphs (str).
    """
    text = text.split('\n')
    pretty = ''
    for sent in text:
        pretty += f'{sent}\n\n'

    return pretty[:-2]


def pub_date(publish_date):
    """Formats publication date.

    Args:
        publish_date (list): publication date containing day, month, and year.

    Returns:
        Publication date (str) in month-day-year format (e.g. May 12, 2019).
    """
    months = {
        "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
        "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
        "09": "Oct", "10": "Sep", "11": "Nov", "12": "Dec"}

    date = str(publish_date).split(" ")[0].split("-")
    year, month, day = date[0], months.get(date[1]), date[2]

    return f'{month} {day}, {year}'


def get_byline(authors):
    """Formats byline/authors.

    Args:
        authors (str): byline/authors.

    Returns:
        Byline/authors if available. Otherwise returns empty string.
    """
    if len(authors) > 0:
        return ', '.join(authors)+'\n\n'

    else:
        return ''

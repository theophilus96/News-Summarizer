from jolt_newspaper import summarised_article
from jolt_user_db import get_user_stories, get_user_scheds, get_user_topics


def main_menu_message():
    """Message for main menu."""

    # the news editor may insert the "Editor's Pick" story in the message here,
    # or customise the message to even send a url such as a YouTube link.
    # any formatting of the message (e.g. bold, italics, urls, and so on) is done in HTML.
    message = """📌 <b>JOLT NEWS BULLETIN</b>"""

    return message


def story_headlines_menu_message(user_id, news_topic):
    """Message for news headlines for seletected news topic."""
    # extract news headlines from bulletin text file
    stories = get_user_stories(user_id, news_topic)

    h_message = ''
    for story in stories:
        num, headline = story[0], story[1]
        h_message += f'{emojify_num(num)} {headline}\n\n'
    h_message.strip()

    if news_topic == 'default':
        news_topic = 'top stories'
        message = f'<b>{news_topic.upper()}</b>\n\n{h_message}'
    else:
        message = f'<b>{news_topic.upper()}</b>\n\n{h_message}'
    return message


def story_message(news_url):
    """Message for story in news bulletin."""

    url = news_url
    title, authors, date, summary = summarised_article(url)
    message = f'<b>{title}</b> – {date}\n\n{authors}{summary}'

    return message


def story_menu_message(news_url):
    """Message containing summarised article."""
    message = story_message(news_url)
    return message


def topic_pref_message(user_id):
    """Bot replies with list of current user preferences for topics."""
    topics = get_user_topics(user_id)
    message = ''
    if topics is None:
        message += "You currently have no topics subscribed. \
Please select some topics below to let me know what to send the next time."

    else:
        message += 'Here are your current preferences:\n'

        for topic in topics:
            if topic.lower() == 'default':
                topic = 'top stories'
            message += f"✅ {topic.title()}\n"
        message += "\nClick on topics below to add or remove a topic. \
Click Save when done."

    return message


def sched_pref_message(user_id):
    """Message for user topic preferences."""
    scheds = get_user_scheds(user_id)
    message = ''
    if scheds is None:
        message += "You currently have no timings subscribed. \
Please select some timings below to let me know what to send the next time."

    else:
        message += 'Here are your current preferences:\n'

        for sched in scheds:
            message += f"✅ {sched.title()}\n"
        message += "\nClick on timings below to add or remove a timing. \
Click Save when done."

    return message


def help_menu_message():
    """Message for help menu."""
    message = """<b>HELP</b>
Hey there! We hope you like using Jolt so far. The Jolt team is working \
on more features for Jolt to help you feel the spark of news again.

In the mean time, here are a list of commands you can invoke:

/start - Fetches news from ST.
/search - Searches ST for stories related to the search query (e.g. \
<i>/search fake news</i>).
/help - Opens help menu."""

    return message


def settings_menu_message():
    """Message for settings menu."""
    message = """⚙ <b>SETTINGS</b>

Choose settings to configure:
- News topics
- Schedule"""

    return message


def pers_topic_message():
    """Message for personalising topic preferences."""
    message = """To start, I'd like to send you news that you care about. \
Please select some topics below if it interests you. Click continue \
when you're done."""

    return message


def sched_topic_message():
    """Message for personalising schedule preferences."""
    message = """Now, I'd like to know when you'd like to have the news. \
Please select your prefered timing(s) below. Click continue \
when you're done."""

    return message


def pers_done_message():
    """Message for the last step in personalising the bot."""
    message = """Great!! We're now good to go and we're ready \
to send you your first bulletin. Click 👉 /start to begin."""

    return message


def welcome_message():
    """Welcome message for new user."""
    message = """Hey there! Welcome to using Jolt, a bot dedicated to help \
you feel the spark of news again!

Let's begin by personalising your news feed. Click on the 'Personalise' \
button below to continue."""

    return message


def emojify_num(num):
    """Returns integer with emoji version."""
    emoji = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣',
             6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣', 10: '🔟'}

    return emoji[num]

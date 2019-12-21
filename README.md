# Jolt, a Telegram news bot

![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)

![jolt](/Users/theophiluskwek/Documents/Github/Jolt/Jolt-Portfolio.png)

We want news readers to start discussions about news they care about and feel empowered by it.

Table of contents:

    1. [Introduction](#introduction)
    2. [Requirements](#requirements)
    3. [Setup](#setup)
    4. [Usage and customisation](#usage-and-customisation)
    5. [Future optimisations](#future-optimisations)
    6. [Acknowledgements](#acknowledgements)
    7. [Team](#team)

# 1. Introduction

Jolt is a Telegram bot for users to read the news from [The Straits Times](https://www.straitstimes.com) and to create their own personal news bulletins.

# 2. Requirements

* bs4 == 0.0.1
* gsearch == 1.6.0
* newspaper3k == 0.2.5
* python\_telegram\_bot == 12.0.0b1

# 3. Setup

1. Create a bot with Telegram's [Bot Father](https://telegram.me/botfather) bot. A guide to creating a bot with Bot Father can be found [here](<https://core.telegram.org/bots#6-botfather>).
2. Pass in the bot's API token to `TOKEN` in `main.py`:
```python
TOKEN = 'token'  # insert token API here
```
3. The bot can search for news based on user messages sent to the bot, either in in a private or group chat. To enable this function, use `@BotFather` to disable [privacy mode](<https://core.telegram.org/bots#privacy-mode>) for the bot.
4. The bot is now ready. Run `main.py` to run the bot.

# 4. Usage and customisation

On the user's first use of Jolt, the user can personalise their news bulletin. The bot will guide the user through setting up their bulletin whilst showing them how to use the inline keyboards to navigate the bulletin's menus.

## News bulletin and topics

The user can subscribe up to 12 broad news topics, which include:

* Top Stories
* Singapore
* Asia
* World
* Politics
* Business
* Lifestyle (and more)

The news bulletin can be pulled from Jolt by sending Jolt the `/start` command. The user can change their settings for topic preferences via the settings menu, which is accessed from the news bulletin menu. For each topic the user subscribes to, the bot will retrieve the top five stories for the user to read.

## Bot menus

Jolt uses [inline keyboards](https://core.telegram.org/bots/2-0-intro#new-inline-keyboards) to build its menus.

##### Main menu
The main menu presents the user with a message from the bot and buttons of news topics that the user has subscribed to. The message of the news bulletin is customisable. If the bot belongs to a news organisation, this message can be edited to send a message from the editor, for example. The message to edit is found in `jolt_messages.py` under the `main_menu_message()` function.

```python
def main_menu_message():
    """Message for main menu."""

    # the news editor may insert the "Editor's Pick" story in the message here,
    # or customise the message to even send a url such as a YouTube link.
    # any formatting of the message (e.g. bold, italics, urls, and so on) is done in HTML.
    message = """📌 <b>JOLT NEWS BULLETIN</b>"""

    return(message)
```

Also on the main menu, users can change their personal preferences via the `⚙️ Settings` button, or update the bulletin with the latest news via the `🆕 Refresh bulletin` button. The help menu is accessed via the `❔ Help` button.

##### Headlines sub-menu
Clicking on the news topics on the main menu brings the user to the top five stories for the particular topic. Users may choose to read any of the five stories, or return to the main menu.

##### News story sub-menu
Clicking to read the story from the headlines sub-menu presents the user with the individual news story, summarised in five lines. They may also choose to read the full story, by clicking the `Full story 📑` button, or toggle to other stories of the same topic using the story's navigation buttons, `◀ Prev` or `Next ▶`. The `↩ Return to stories` button returns the user to the headlines sub-menu of the same news topic.

## Bot Commmands

Jolt accepts commands sent as messages by the user to the bot. Commands always begin with a forward slash `/`, proceeded immediately by the command word.

Jolt has the following commands:

##### `/start`

* Send `/start` to scrape news from ST.com and build the news bulletin. Once done, the bot sends the bulletin to the user/chat group.


##### `/search`

* Use this command, followed by a search query (e.g. `/search fake news laws`), to search for the query using Google's search engine. Jolt will return the user with five of the latest stories relating to the query.

##### `/help`

* Send `/help` to open up the help menu.

## Search latest news

There are three ways to search for news using Jolt:

1. Using `/search`. Typing `/search <query>` and sending the message to Jolt prompts the bot to search for the user's query, `<query>`.
2. Mentioning `@jolt_newsbot`. Similar to `/search`, mentioning Jolt in a message followed by a query `@jolt_newsbot <query>` prompts the bot to search for the query. This method of searching works in group chats only if privacy mode is disabled for the bot, since the bot would need to have access to the chat messages.
3. Sending a message to Jolt in a private chat. Sending a message to Jolt in a private chat immediately prompts the bot to search for the message as a search query. For example, sending `what happens to cersei in game of thrones?` will prompt the bot to search for 'what happens to cersei in game of thrones?'. Sending messages in group chats where the bot is a member will not prompt the bot to make any searches.

Upon a successful search, Jolt will return the user with the five most recent stories (from ST.com) related to the search query. An image from the first article will be included in the search result.

## Schedule 

__[Work-in-progress]__ Users can also choose to have the news bulletin sent to them daily, during different times of the day. The timings can be changed from the settings menu.

# 5. Future optimisations

We hope to improve and add on to Jolt's current capabilities. These include:

* Having a better UX, such as smoother tutorials for first-time users.
* Being able to handle conversations in a casual or more organic manner.
* Being able to subsrcribe to specific news tags or keywords.
* Being able 'like' news stories to gauge its popularity.
* Having interactive quizzes.
* Enabling different types of content such as videos and podcasts to be easily accessible.

# 6. Acknowledgements

We would like to thank our news partners at The Straits Times, Sandra Davie and Azhar Kasman, and our mentor at Google, Kate Beddoe, for their expert guidance. We would also like to extend our thanks to our first prototype users, Lin Shan, Gracia, and Melissa, for their invaluable feedback. Lastly, we want to thank our instructors Jessica Tan and Joan Kelly for their continuous support and encouragement during our design thinking process.

# 7. Team

Anthony, Christy, Iskandar, Kenneth, Michael, and Theophilus.

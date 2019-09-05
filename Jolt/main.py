"""
JOLT TELEGRAM NEWS BOT
"""

import logging
import os

from jolt_keyboardbuttons import *
from jolt_messsages import *

from jolt_bulletin import missed_news
from jolt_bulletin import news_bulletin
from jolt_search import google_search
from jolt_newspaper import get_news_pic

from jolt_user_db import create_user_db
from jolt_user_db import get_chat_data
from jolt_user_db import get_user_scheds
from jolt_user_db import get_user_stories
from jolt_user_db import get_user_topics
from jolt_user_db import toggle_setting

from telegram import ParseMode
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater


def start(update, context):
    """Usage: /start"""
    # get user particulars
    data = update.message
    chat_type = get_chat_data(data, chat_type=True)  # private/group
    user_id = get_chat_data(data, user_id=True)  # private/group id
    username = get_chat_data(data, username=True)  # username/chat group name

    # check if user has existing json file for config settings.
    user_db_exists = os.path.isfile(f'{user_id}_config.json')

    if user_db_exists is False:
        # user database is absent - i.e. new user
        # create user database
        create_user_db(user_id, username, chat_type)
        print('[NEW USER]', user_id, username)

        # send 'hello!' gif
        gif = 'https://media.giphy.com/media/dzaUX7CAG0Ihi/giphy.gif'
        context.bot.send_animation(
            chat_id=user_id,
            animation=gif,
            duration=10)

        # send welcome message, start personalisation
        update.message.reply_text(
            text=welcome_message(),
            reply_markup=start_personalise_menu_keyboard(),
            parse_mode=ParseMode.HTML)

    else:
        # user has existing data - i.e. config settings
        # start news bulletin, send wait message as news bulletin is building
        wait_message = context.bot.send_message(
            chat_id=user_id,
            text='Jolt is fetching your news. BRB.')

        # bot will scrape ST.com for news, write headlines and urls into
        # json files, which will be accessed later to create headlines
        # and summaries of each story for the news bulletin
        news_bulletin(user_id)

        # check if scraper has missed out any news
        # if news is missing, scrape again; stop scrape after third retry
        retry = 0
        while missed_news(user_id) is True:
            context.bot.edit_message_text(
                chat_id=user_id,
                message_id=wait_message.message_id,
                text=f'Oops! I may have missed out something. Retrying ({retry})...'
                )
            news_bulletin(user_id)  # scrape again
            retry += 1

            if retry == 4:
                context.bot.edit_message_text(
                    chat_id=user_id,
                    message_id=wait_message.message_id,
                    text='Retry cancelled. Some stories might be missing. /start to try again.'
                    )
                break

        print('[JOLT BULLETIN SENT]', user_id, username)

        # if scrape is successful, show news bulletin's main menu
        context.bot.send_message(
            chat_id=user_id,
            text='@jolt_newsbot',
            reply_markup=main_menu_replykeyboard(),
            disable_web_page_preview=False,
            parse_mode=ParseMode.HTML)

        context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            message_id=wait_message.message_id,
            text=main_menu_message(),
            reply_markup=main_menu_keyboard(user_id),
            disable_web_page_preview=False,
            parse_mode=ParseMode.HTML)


def main_menu(update, context):
    """Main menu - shows news topics and settings."""
    query = update.callback_query
    print('[QUERY] main menu:', query.data)

    topic = query.data.split('_')[0]
    user_id = get_chat_data(query, user_id=True)

    # return to main menu
    if (query.data == 'main' or query.data == 'refresh'):
        if query.data == 'refresh':
            query.edit_message_text(
                text='Jolt is fetching your news. BRB.',
                parse_mode=ParseMode.HTML)
            news_bulletin(user_id)

        query.edit_message_text(
            text=main_menu_message(),
            reply_markup=main_menu_keyboard(user_id),
            disable_web_page_preview=False,
            parse_mode=ParseMode.HTML)

    # open settings menu
    elif query.data == 'settings':
        query.edit_message_text(
            text=settings_menu_message(),
            reply_markup=settings_menu_keyboard(),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML)

    # open help menu
    elif query.data == 'help':
        query.edit_message_text(
            text=help_menu_message(),
            reply_markup=help_menu_keyboard(),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML)

    # open headline menu from topic
    elif topic.isalpha():
        query.edit_message_text(
            text=story_headlines_menu_message(user_id, topic),
            reply_markup=story_headlines_menu_keyboard(topic),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML)


def setup_tutorial_menu(update, context):
    """Menu for initial setup of personal preferences and tutorial.

    This menu deals specifically with the user setting up their
    personal preferences for the first time.
    """
    query = update.callback_query
    user_id = get_chat_data(query, user_id=True)

    # get user's subscription to topics and schedules
    # on user's first use of the bot, subbed_topics and
    # subbed_scheds should return None.
    subbed_topics = get_user_topics(user_id)
    subbed_scheds = get_user_scheds(user_id)

    if query.data == 'p-topics':
        # show menu to setup topic preferences
        query.edit_message_text(
            text=pers_topic_message(),
            reply_markup=pers_topic_menu_keyboard(),
            parse_mode=ParseMode.HTML)

    elif query.data.startswith('!'):
        # toggle topic's setting between True/False
        topic = query.data[1:]
        state = toggle_setting(user_id, 'topics', topic)

        message = ''  # message for when topics are added/removed
        if state is True:
            if topic == 'default':
                topic = 'Top Stories'
            message += f'Added ⭕ "{topic.title()}".\n\n'
        elif state is False:
            message += f'Removed ❌ "{topic.title()}".\n\n'
        message += topic_pref_message(user_id).replace('Save', 'Continue')

        query.edit_message_text(
            text=message,
            reply_markup=pers_topic_menu_keyboard(),
            parse_mode=ParseMode.HTML)

    elif query.data == 'p-sched':

        while subbed_topics is None:
            # if user has no topics, prompt user to select topic
            query.edit_message_text(
                text='ℹ Please add at least one topic to continue.',
                reply_markup=pers_topic_menu_keyboard(),
                parse_mode=ParseMode.HTML)

        # show menu to setup schedule preferences
        query.edit_message_text(
            text=sched_topic_message(),
            reply_markup=pers_sched_menu_keyboard(),
            parse_mode=ParseMode.HTML)

    elif query.data.startswith('&'):
        # toggle topic's setting between True/False
        sched = query.data.split('-')[1]
        state = toggle_setting(user_id, 'schedule', sched)

        message = ''  # message for when timings are added/removed
        if state is True:
            message += f'Added ⭕ "{sched.title()}".\n\n'
        elif state is False:
            message += f'Removed ❌ "{sched.title()}".\n\n'
        message += sched_pref_message(user_id).replace('Save', 'Continue')

        query.edit_message_text(
            text=message,
            reply_markup=pers_sched_menu_keyboard(),
            parse_mode=ParseMode.HTML)

    elif query.data == 'p-done':

        while subbed_scheds is None:
            # if user has no timings, prompt user to select timing
            query.edit_message_text(
                text='ℹ Please add at least one timing to continue.',
                reply_markup=pers_sched_menu_keyboard(),
                parse_mode=ParseMode.HTML)

        # personalisation done,
        # continue to start first bulletin
        query.edit_message_text(
            text=pers_done_message())


def settings_menu(update, context):
    """Settings menu."""
    query = update.callback_query
    user_id = get_chat_data(query, user_id=True)

    if query.data == 'set-topic':
        # show menu to set topic preferences
        query.edit_message_text(
            text=topic_pref_message(user_id),
            reply_markup=topic_pref_menu_keyboard(),
            parse_mode=ParseMode.HTML)

    elif query.data == 'set-sched':
        # show menu to set schedule preferences
        query.edit_message_text(
            text=sched_pref_message(user_id),
            reply_markup=sched_pref_menu_keyboard(),
            parse_mode=ParseMode.HTML)


def sched_pref_menu(update, context):
    """Menu for choosing schedule."""
    query = update.callback_query
    user_id = get_chat_data(query, user_id=True)

    sched = query.data.split('-')[1]
    message = ''  # message for when timings are added/removed
    state = toggle_setting(user_id, 'schedule', sched)
    if state is True:
        message += f'Added ⭕ "{sched.title()}".\n\n'
    elif state is False:
        message += f'Removed ❌ "{sched.title()}".\n\n'
    message += sched_pref_message(user_id)

    query.edit_message_text(
        text=message,
        reply_markup=sched_pref_menu_keyboard(),
        parse_mode=ParseMode.HTML)


def topic_pref_menu(update, context):
    """Menu for choosing topic preferences."""
    query = update.callback_query
    user_id = get_chat_data(query, user_id=True)

    # toggle topic's setting between True/False
    topic = query.data[1:]
    state = toggle_setting(user_id, 'topics', topic)

    message = ''  # message for when topics are added/removed
    if state is True:
        if topic == 'default':
            topic = 'Top Stories'
        message += f'Added ⭕ "{topic.title()}".\n\n'
    elif state is False:
        message += f'Removed ❌ "{topic.title()}".\n\n'

    query.edit_message_text(
        text=message+topic_pref_message(user_id),
        reply_markup=topic_pref_menu_keyboard(),
        parse_mode=ParseMode.HTML)


def story_headlines_menu(update, context):
    """Menu for first story."""
    query = update.callback_query
    user_id = get_chat_data(query, user_id=True)
    print('[QUERY] headlines menu:', query.data)

    # return to story headlines menu
    topic = query.data.split('-')[0]
    query.edit_message_text(
        text=story_headlines_menu_message(user_id, topic),
        reply_markup=story_headlines_menu_keyboard(topic),
        disable_web_page_preview=True,
        parse_mode=ParseMode.HTML)


def story_menu(update, context):
    """Menu for choosing top 5 stories for a given news category."""
    query = update.callback_query
    user_id = get_chat_data(query, user_id=True)

    # seperate topic from story's sequence number in query
    query_data = query.data.split('_')
    topic, seq_num = query_data[0], int(query_data[1])

    # get stories/headlines (for corresponding topic) from user's json file
    news = get_user_stories(user_id, topic)

    # show correct navigation menu for each story the user selects.
    # each story's menu will have buttons to the previous/next story,
    # as well as a button leading to ST.com to read the full story.
    if seq_num == 1:
        # if first story was selected, then show first story's summary
        # and its corresponding keyboard menu buttons.
        num, headline, url = news[0]
        query.edit_message_text(
            text=story_menu_message(url),
            reply_markup=story_menu_keyboard(topic, url, seq_num=num),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML)

    elif seq_num == 5:
        # if fifth story was selected, then show fifth story's summary
        # and its corresponding keyboard menu buttons.
        num, headline, url = news[-1]
        query.edit_message_text(
            text=story_menu_message(url),
            reply_markup=story_menu_keyboard(topic, url, seq_num=num),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML)

    else:
        # if another story was selected (i.e. not first or last story), then
        # show the story's summar and its corresponding keyboard menu buttons.
        for (num, headline, url) in news:
            if seq_num == num:
                query.edit_message_text(
                    text=story_menu_message(url),
                    reply_markup=story_menu_keyboard(
                        topic, url, seq_num=num),
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.HTML)
                break


def search(update, context):
    """Search function. Usage: /search"""
    query = ' '.join(context.args)
    print(f'[SEARCH] "{query}" (frm cmd)')

    searching = context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"🔎 Searching for '{query}'...")

    results = google_search(query)
    if results is None:
        # tell user that no results found
        context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            message_id=searching.message_id,
            text=f"❌ No results were found for '{query}'.")
    else:
        # tell user the search results
        headline, url = results[0]
        pic = get_news_pic(url)

        message = f"🔎 Here are the latest stories for '{query}':\n\n"
        for count, (headline, url) in enumerate(results, start=1):
            message += f'{emojify_num(count)} {headline} <a href="{url}">READ HERE</a>\n\n'

        context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=pic)
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=message,
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML)


def message_search(update, context):
    """Search for a query from message sent by user."""
    data = update.message
    chat_type = get_chat_data(data, chat_type=True)
    in_message = data.text

    # search from user message
    query = ''
    if in_message.startswith('@jolt_newsbot'):
        # mentioning the bot turns into a search query for news
        query += in_message.partition(' ')[2]

        print(f'[SEARCH] "{query}" (@jolt, {chat_type})')

    elif chat_type == 'group':
        # ignore messages sent in a group chat
        # unless @jolt_newsbot is mentioned
        return

    else:
        # in a private chat with bot, text messages sent to bot
        # becomes search queries to search for news
        query += in_message
        print(f'[SEARCH] "{query}" (frm msg)')

    searching = context.bot.send_message(
        chat_id=data.chat_id,
        text=f"🔎 Searching for '{query}'...")

    results = google_search(query)
    if results is None:
        # tell user that no results found
        context.bot.edit_message_text(
            chat_id=data.chat_id,
            message_id=searching.message_id,
            text=f"❌ No results were found for '{query}'.")
    else:
        # tell user the search results
        headline, url = results[0]
        pic = get_news_pic(url)

        message = f"🔎 Here are the latest stories for '{query}':\n\n"
        for count, (headline, url) in enumerate(results, start=1):
            message += f'{emojify_num(count)} {headline} <a href="{url}">READ HERE</a>\n\n'

        context.bot.send_photo(
            chat_id=data.chat_id,
            photo=pic)
        context.bot.send_message(
            chat_id=data.chat_id,
            text=message,
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML)


def unknown(update, context):
    """Bot replies to all commands that were not recognized by the handlers."""
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Sorry, 🤔 I didn't understand that command.")


def help_me(update, context):
    """Help menu. Usage: /help"""
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=help_menu_message(),
        parse_mode=ParseMode.HTML)


def main():
    """Start the bot."""

    # enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # create the Updater and pass it your bot's token.
    # make sure to set use_context=True to use the new context based callbacks.
    TOKEN = 'token'  # insert token API here

    updater = Updater(token=TOKEN, use_context=True)

    # get dispatcher to register handlers
    dp = updater.dispatcher

    # initiate the following handlers
    # command handlers
    dp.add_handler(CommandHandler('start', start))  # fetch bulletin
    dp.add_handler(CommandHandler('search', search))
    dp.add_handler(CommandHandler('help', help_me))

    #  callback query handlers
    dp.add_handler(CallbackQueryHandler(main_menu,
                                        pattern='^[a-z]*$'))
    dp.add_handler(CallbackQueryHandler(story_headlines_menu,
                                        pattern='^[a-z]*-hl$'))
    dp.add_handler(CallbackQueryHandler(story_menu,
                                        pattern='^[a-z]*_\d*$'))
    dp.add_handler(CallbackQueryHandler(topic_pref_menu,
                                        pattern='^[#][a-z]*$'))
    dp.add_handler(CallbackQueryHandler(sched_pref_menu,
                                        pattern='^sched-[a-z]*$'))
    dp.add_handler(CallbackQueryHandler(setup_tutorial_menu,
                                        pattern='^p-[a-z]*$|^[!]|^[&]'))
    dp.add_handler(CallbackQueryHandler(settings_menu,
                                        pattern='^set-[a-z]*$'))

    # message handlers
    dp.add_handler(MessageHandler(Filters.text, message_search))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # start the bot
    updater.start_polling()
    print('Jolt is running.')
    updater.idle()


if __name__ == '__main__':
    main()

from jolt_user_db import get_user_topics

from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def main_menu_replykeyboard():
    """Reply keyboard for main menu."""

    keyboard = [[InlineKeyboardButton("/start")]]
    return ReplyKeyboardMarkup(keyboard,
                               one_time_keyboard=False,
                               resize_keyboard=True)


def main_menu_keyboard(user_id):
    """Keyboard for main menu."""
    topics = get_user_topics(user_id)
    buttons_list = build_menu(topics, n_cols=2)
    keyboard = []
    for row in buttons_list:
        new_row = []
        for item in row:
            new_row += [InlineKeyboardButton(
                button_text_emoji(item),  # text for button
                callback_data=item  # callback for button
                )
            ]
        keyboard.append(new_row)

    # add additional buttons below news topic buttons
    help_button = InlineKeyboardButton("❔ Help", callback_data='help')
    about_button = InlineKeyboardButton("⚡ About Jolt",
                                        url='https://www.behance.net/gallery/78925047/Jolt-UX-Design',
                                        callback_data='about')
    refresh_button = InlineKeyboardButton("🆕 Refresh bulletin", callback_data='refresh')
    settings_button = InlineKeyboardButton("⚙️ Settings", callback_data='settings')

    keyboard.append([about_button, help_button])
    keyboard.append([refresh_button])
    keyboard.append([settings_button])

    return InlineKeyboardMarkup(keyboard)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    """Builds menu based on list of strings.

    Args:
        buttons (list): list of strings.
        n_cols (str): number of columns.
        header_buttons (list): list of strings for header button. Defaults to None.
        footer_buttons (list): list of strings for footer button. Defaults to None.

    Returns:
        List of buttons (str).
    """
    if len(buttons) % 2 != 0:
        buttons.append('—')  # create filler button

    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def story_headlines_menu_keyboard(topic):
    """Keyboard for headlines submenu"""
    keyboard = [[InlineKeyboardButton("Read 1️⃣",
                                      callback_data=f'{topic}_1'),
                 InlineKeyboardButton("Read 2️⃣",
                                      callback_data=f'{topic}_2')],
                [InlineKeyboardButton("Read 3️⃣",
                                      callback_data=f'{topic}_3'),
                 InlineKeyboardButton("Read 4️⃣",
                                      callback_data=f'{topic}_4')],
                [InlineKeyboardButton("Read 5️⃣",
                                      callback_data=f'{topic}_5'),
                 InlineKeyboardButton("↩ Return", callback_data='main')]]

    return InlineKeyboardMarkup(keyboard)


def settings_menu_keyboard():
    """Keyboard menu buttons for settings menu."""
    keyboard = [[InlineKeyboardButton("📬 Topics",
                                      callback_data='set-topic'),
                 InlineKeyboardButton("⏰ Schedule",
                                      callback_data='set-sched')],
                [InlineKeyboardButton("↩ Return",
                                      callback_data='main')]]

    return InlineKeyboardMarkup(keyboard)


def pers_topic_menu_keyboard():
    """Keyboard for setting up initial topic preferences."""
    keyboard = [[InlineKeyboardButton("💎 Top Stories",
                                      callback_data='!default'),
                 InlineKeyboardButton("🇸🇬 Singapore",
                                      callback_data='!singapore')],
                [InlineKeyboardButton("🏯 Asia",
                                      callback_data='!asia'),
                 InlineKeyboardButton("🌍 World",
                                      callback_data='!world')],
                [InlineKeyboardButton("🏛 Politics",
                                      callback_data='!politics'),
                 InlineKeyboardButton("📈 Business",
                                      callback_data='!business')],
                [InlineKeyboardButton("🎭 Lifestyle",
                                      callback_data='!lifestyle'),
                 InlineKeyboardButton("🏆 Sport",
                                      callback_data='!sport')],
                [InlineKeyboardButton("🎓 Education",
                                      callback_data='!education'),
                 InlineKeyboardButton("🔬 Science",
                                      callback_data='!science')],
                [InlineKeyboardButton("♻️ Environment",
                                      callback_data='!environment'),
                 InlineKeyboardButton("⚕️ Health",
                                      callback_data='!health')],
                [InlineKeyboardButton("Continue ➡️",
                                      callback_data='p-sched')]]

    return InlineKeyboardMarkup(keyboard)


def pers_sched_menu_keyboard():
    """Keyboard for choosing schedule preference."""
    keyboard = [[InlineKeyboardButton("🌅 Morning",
                                      callback_data='&sched-morning')],
                [InlineKeyboardButton("⛅ Afternoon",
                                      callback_data='&sched-afternoon')],
                [InlineKeyboardButton("🌇 Evening",
                                      callback_data='&sched-evening')],
                [InlineKeyboardButton("Continue ➡️",
                                      callback_data='p-done')]]

    return InlineKeyboardMarkup(keyboard)


def topic_pref_menu_keyboard():
    """Keyboard for choosing topic preferences."""
    keyboard = [[InlineKeyboardButton("💎 Top Stories",
                                      callback_data='#default'),
                 InlineKeyboardButton("🇸🇬 Singapore",
                                      callback_data='#singapore')],
                [InlineKeyboardButton("🏯 Asia",
                                      callback_data='#asia'),
                 InlineKeyboardButton("🌍 World",
                                      callback_data='#world')],
                [InlineKeyboardButton("🏛 Politics",
                                      callback_data='#politics'),
                 InlineKeyboardButton("📈 Business",
                                      callback_data='#business')],
                [InlineKeyboardButton("🎭 Lifestyle",
                                      callback_data='#lifestyle'),
                 InlineKeyboardButton("🏆 Sport",
                                      callback_data='#sport')],
                [InlineKeyboardButton("🎓 Education",
                                      callback_data='#education'),
                 InlineKeyboardButton("🔬 Science",
                                      callback_data='#science')],
                [InlineKeyboardButton("♻️ Environment",
                                      callback_data='#environment'),
                 InlineKeyboardButton("⚕️ Health",
                                      callback_data='#health')],
                [InlineKeyboardButton("Save! 💾",
                                      callback_data='refresh')]]

    return InlineKeyboardMarkup(keyboard)


def sched_pref_menu_keyboard():
    """Keyboard for choosing schedule preferences."""
    keyboard = [[InlineKeyboardButton("🌅 Morning",
                                      callback_data='sched-morning')],
                [InlineKeyboardButton("⛅ Afternoon",
                                      callback_data='sched-afternoon')],
                [InlineKeyboardButton("🌇 Evening",
                                      callback_data='sched-evening')],
                [InlineKeyboardButton("Save! 💾",
                                      callback_data='refresh')]]

    return InlineKeyboardMarkup(keyboard)


def start_personalise_menu_keyboard():
    """Keyboard menu for first time setting up topic preferences."""
    keyboard = [[InlineKeyboardButton("Personalise ✨",
                                      callback_data='p-topics')]]

    return InlineKeyboardMarkup(keyboard)


def story_menu_keyboard(topic, url, seq_num):
    """Keyboard for individual news story."""
    keyboard = list()
    if seq_num == 1:
        keyboard += [[InlineKeyboardButton("Next ▶",
                                           callback_data=f'{topic}_2'),
                      InlineKeyboardButton("Full story 📑", url=f'{url}',
                                           callback_data=f'{topic}-full')],
                     [InlineKeyboardButton("↩ Return to stories",
                                           callback_data=f'{topic}-hl')]]
    elif seq_num == 5:
        keyboard += [[InlineKeyboardButton("◀ Prev",
                                           callback_data=f'{topic}_4'),
                      InlineKeyboardButton("Full story 📑", url=f'{url}',
                                           callback_data=f'{topic}-full')],
                     [InlineKeyboardButton("↩ Return to stories",
                                           callback_data=f'{topic}-hl')]]
    else:
        prev_story = seq_num-1
        next_story = seq_num+1
        keyboard += [[InlineKeyboardButton("◀ Prev",
                                           callback_data=f'{topic}_{prev_story}'),
                      InlineKeyboardButton("Full story 📑", url=f'{url}',
                                           callback_data=f'{topic}-full'),
                      InlineKeyboardButton("Next ▶",
                                           callback_data=f'{topic}_{next_story}')],
                     [InlineKeyboardButton("↩ Return to stories",
                                           callback_data=f'{topic}-hl')]]

    return InlineKeyboardMarkup(keyboard)


def help_menu_keyboard():
    """Keyboard buttons for help menu."""
    keyboard = [[InlineKeyboardButton("↩ Return", callback_data='main')]]

    return InlineKeyboardMarkup(keyboard)


def button_text_emoji(text):
    """Emoji for buttons.

    Args:
        text (str): text to pair emoji with.

    Returns:
        Text with emoji if successful. Otherwise, returns text only.
    """
    emojis = {'default'     : '💎',
              'singapore'   : '🇸🇬',
              'asia'        : '🏯',
              'world'       : '🌍',
              'politics'    : '🏛',
              'business'    : '📈',
              'lifestyle'   : '🎭',
              'sport'       : '🏆',
              'education'   : '🎓',
              'science'     : '🔬',
              'environment' : '♻️',
              'health'      : '⚕️'
              }

    try:
        emoji = emojis[text]
        if text == 'default':
            text = 'Top Stories'
        emoji_text = emoji + ' ' + text.title()
        return emoji_text

    except KeyError:
        return text

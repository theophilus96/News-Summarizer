import json


def write_to_json(file_name, data, path='./'):
    """Writes data to json file.

    Args:
        file_name (str): file name for json file.
        data (dict): data to write to json file.
        path (str): path to write json file. Defaults to current folder.

    Returns:
        None.
    """
    json_file = './' + path + '/' + str(file_name) + '_config.json'
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    return


def create_user_db(user_id, user_name, chat_type):
    """Creates a json file to store user data.

    Args:
        user_id (int): user id.
        user_name(str): username.
        chat_type (str): type of chat (private/group).

    Returns:
        None.
    """
    # user's topics for news bulletin
    # 'default' (i.e. top stories) is True by default
    topics = {'default'     : False,
              'singapore'   : False,
              'asia'        : False,
              'world'       : False,
              'politics'    : False,
              'business'    : False,
              'lifestyle'   : False,
              'sport'       : False,
              'education'   : False,
              'science'     : False,
              'environment' : False,
              'health'      : False
              }

    # user's schedule
    # work-in-progress: the aim is to have the bot send the
    # news bulletin at the following timings.
    # 'morning' is True by default
    schedule = {'morning'   : False,     # 0700 hours
                'afternoon' : False,    # 1300 hours
                'evening'   : False     # 1800 hours
                # 'custom'    : False   # custom time set by user
                }

    bulletin = {}  # stores news articles headlines and urls

    # user data to be written into json file
    user_data = {'username' : user_name,
                 'id'       : user_id,
                 'chat_type': chat_type,
                 'topics'   : topics,
                 'schedule' : schedule,
                 'bulletin' : bulletin
                 }

    # write user's data to json file,
    # creates json file if file doesn't exist
    write_to_json(user_id, user_data)

    return


def get_user_data(user_id):
    """Get user data from user json file.

    Args:
        user_id (int): user id.

    Returns:
        User data (dict).
    """
    json_file = f'{user_id}_config.json'
    with open(json_file, 'r') as f:
        data = json.load(f)

    return(data)


def toggle_setting(user_id, key, subkey):
    """ Toggles setting for key-subkey pair between True and False.
    Updates user's json file accordingly. Returns new state of setting.

    Args:
        user_id (int): user id.
        key (str): setting category (e.g. 'topics', 'schedule')
        subkey (str): setting within category

    Returns:
        True if previous setting was False and vice versa.
    """
    state = None
    json_file = f'{user_id}_config.json'
    with open(json_file, 'r') as f:
        data = json.load(f)

        # find relevant key and subkey
        if data[f'{key}'][f'{subkey}'] is False:
            data[f'{key}'][f'{subkey}'] = True
            state = True
        else:
            data[f'{key}'][f'{subkey}'] = False
            state = False

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    return state


def get_user_stories(user_id, news_topic):
    """Get all news headlines and url for a news topic.

    Args:
        user_id (int): user id.
        news_topic (str): news topic.

    Returns:
        List of headlines and urls for news topic.
    """
    data = get_user_data(user_id)
    headlines = data['bulletin'][news_topic]

    return headlines


def get_user_topics(user_id):
    """Get topics from user that are True

    Args:
        user_id (int): user id.

    Returns:
        List of user-chosen topics if successful, None otherwise.
    """
    data = get_user_data(user_id)
    topics = data['topics']
    user_topics = list()
    for topic, value in topics.items():
        if value is True:
            # add topic to user topics
            user_topics.append(topic)

    if len(user_topics) == 0:
        return

    else:
        return user_topics


def get_user_scheds(user_id):
    """Get schedule from user that are True.

    Args:
        user_id (int): user id.

    Returns:
        List of user-chosen timings if successful, None otherwise.
    """
    data = get_user_data(user_id)
    scheds = data['schedule']
    user_scheds = list()
    for sched, value in scheds.items():
        if value is True:
            user_scheds.append(sched)

    if len(user_scheds) == 0:
        return

    else:
        return user_scheds


def get_chat_data(data, user_id=None, username=None, chat_type=None):
    """Returns user id/username/chat type from message data"""
    get_data = None
    if user_id is True:
        get_data = get_chat_user_id(data)
    elif username is True:
        get_data = get_chat_username(data)
    elif chat_type is True:
        get_data = get_chat_type(data)
    else:
        return

    return get_data


def get_chat_user_id(query):
    """Returns user id from message data."""
    data = eval(str(query))
    try:
        chat = data['message']['chat']
    except KeyError:
        chat = data['chat']
    user_id = chat['id']

    return user_id


def get_chat_username(query):
    """Returns username from message data."""
    data = eval(str(query))
    chat_type = get_chat_type(query)

    if chat_type == 'private':
        username = data['chat']['username']
        return username

    elif chat_type == 'group':
        title = data['chat']['title']
        return title

    else:
        return


def get_chat_type(query):
    """Returns chat type from message data."""
    data = eval(str(query))

    try:
        chat = data['message']['chat']
    except KeyError:
        chat = data['chat']
    chat_type = chat['type']

    return chat_type

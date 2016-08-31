from trello_api import api_url, list_name_convert
import ConfigParser
import requests
import json
import os
import sys

authkeys_filename = 'authkeys.cfg'
itemids_filename = 'itemids.cfg'
cfg_filepath = os.path.dirname(os.path.realpath(__file__))


def get_auth_args():
    config = ConfigParser.ConfigParser()
    read = config.read(os.path.join(cfg_filepath, authkeys_filename))

    if not read:
        return set_authkeys()
    else:
        auth_args = 'key=%s&token=%s' % (config.get('AuthKeys', 'app_key'),
                                         config.get('AuthKeys', 'auth_token'))
        return auth_args


def get_item_ids():
    config = ConfigParser.ConfigParser()
    read = config.read(os.path.join(cfg_filepath, itemids_filename))

    if not read:
        return set_itemids(get_auth_args())
    else:
        item_ids = {
            'board': config.get('ItemIds', 'board'),
            'iu': config.get('ItemIds', 'iu'),
            'inu': config.get('ItemIds', 'inu'),
            'uu': config.get('ItemIds', 'uu'),
            'unu': config.get('ItemIds', 'unu'),
            'done': config.get('ItemIds', 'done'),
        }
        return item_ids


def set_authkeys():
    """ Sets up the CLI by creating a config file containing the user's
    Trello app key and auth token.
    :return: str
    """
    print "Yo, welcome to YoDoIt!"
    auth_keys = {}
    auth_keys['app_key'] = raw_input("Yo, enter your Trello app key: ")
    auth_keys['auth_token'] = raw_input("Yo, enter your Trello auth token: ")

    # Validate app key and auth token by doing a bogus search query
    auth_args = 'key=%s&token=%s' % (auth_keys['app_key'], auth_keys['auth_token'])
    test_request = requests.get('%s/search?query=%s&%s' % (api_url, 'yodoit_test_auth', auth_args))

    if test_request.status_code != requests.codes.ok:
        print "Invalid app key and/or auth token."
        sys.exit(1)
    else:
        write_cfg_authkeys_file(auth_keys)
        print "Yo, your Trello account is hooked up with YoDoIt!"
        return auth_args


def set_itemids(auth_args):
    """ Sets up the CLI by creating a config file containing the user's
    Trello board item IDs.
    :param auth_args: str
    :return:
    """
    board_type = raw_input(
        "Yo, do you wanna use a new board or an existing board? (new/existing): ")
    if board_type == 'new':
        return set_new_board(auth_args)
    elif board_type == 'existing':
        return set_existing_board(auth_args)
    else:
        print "Invalid input."
        sys.exit(1)


def set_new_board(auth_args):
    board_name = "YoDoIt!"
    board_desc = "A simple decision making tool to help you be more productive."

    post_board_url = '%s/boards?name=%s&desc=%s&%s' % (api_url, board_name, board_desc, auth_args)
    request = requests.post(post_board_url)
    board = json.loads(request.text)

    item_ids = {}
    item_ids['board'] = board['id']
    empty_new_board(auth_args, item_ids)
    add_yodoit_lists(auth_args, item_ids)
    write_cfg_itemids_file(item_ids)
    print "Yo, your new board is set!"
    return item_ids


def empty_new_board(auth_args, item_ids):
    """ Archives all lists in a board. Needed because when creating a board
    with Trello API, 3 default lists are created.
    :param auth_args:
    :param item_ids:
    :return:
    """
    get_lists_url = '%s/boards/%s/lists?%s' % (api_url, item_ids['board'], auth_args)
    request = requests.get(get_lists_url)

    lists = json.loads(request.text)
    for list in lists:
        list_id = list['id']
        put_list_url = '%s/lists/%s/closed?value=true&%s' % (api_url, list_id, auth_args)
        requests.put(put_list_url)


def add_yodoit_lists(auth_args, item_ids):
    """ Adds the 4 Eisenhower Decision Matrix categories + Done as lists to
    a board.
    :param auth_args:
    :param item_ids:
    :return:
    """
    done = requests.post('%s/boards/%s/lists?name=%s&%s' % (api_url, item_ids['board'], 'Done', auth_args))
    item_ids['done'] = json.loads(done.text)['id']
    unu = requests.post('%s/boards/%s/lists?name=%s&%s' % (api_url, item_ids['board'], 'Unimportant Not Urgent', auth_args))
    item_ids['unu'] = json.loads(unu.text)['id']
    uu = requests.post('%s/boards/%s/lists?name=%s&%s' % (api_url, item_ids['board'], 'Unimportant Urgent', auth_args))
    item_ids['uu'] = json.loads(uu.text)['id']
    inu = requests.post('%s/boards/%s/lists?name=%s&%s' % (api_url, item_ids['board'], 'Important Not Urgent', auth_args))
    item_ids['inu'] = json.loads(inu.text)['id']
    iu = requests.post('%s/boards/%s/lists?name=%s&%s' % (api_url, item_ids['board'], 'Important Urgent', auth_args))
    item_ids['iu'] = json.loads(iu.text)['id']


def set_existing_board(auth_args):
    print "Yo, go to your Trello board and get its board ID from the url\n" \
          "Example: trello.com/b/[board ID]/[board name]"
    item_ids = {}
    item_ids['board'] = raw_input("Trello board ID: ")
    try:
        request = requests.get("%s/boards/%s/lists?%s" % (api_url, item_ids['board'], auth_args))
        request.raise_for_status()
    except requests.exceptions.HTTPError:
        print "Invalid board ID."
        sys.exit(1)
    lists = json.loads(request.text)
    item_ids['board'] = lists[0]['idBoard']  # Replace short ID with long

    expected_list_names = {'important urgent', 'important not urgent',
                           'unimportant urgent', 'unimportant not urgent',
                           'done'}
    for list in lists:
        if list['name'].lower() in expected_list_names:
            item_ids[list_name_convert[list['name'].lower()]] = list['id']

    # Validate board contents
    for k, v in item_ids.iteritems():
        if not v:
            print (
                "Invalid board. Your board must contain the following lists:"
                "\nImportant Urgent"
                "\nImportant Not Urgent"
                "\nUnimportant Urgent"
                "\nUnimportant Not Urgent"
                "\nDone")
            sys.exit(1)

    write_cfg_itemids_file(item_ids)
    print "Yo, your existing board is set!"
    return item_ids


def write_cfg_authkeys_file(auth_keys):
    config = ConfigParser.ConfigParser()
    config.add_section('AuthKeys')
    config.set('AuthKeys', 'app_key', auth_keys['app_key'])
    config.set('AuthKeys', 'auth_token', auth_keys['auth_token'])

    f = open(os.path.join(cfg_filepath, authkeys_filename), 'w')
    config.write(f)
    f.close()


def write_cfg_itemids_file(item_ids):
    config = ConfigParser.ConfigParser()
    config.add_section('ItemIds')
    config.set('ItemIds', 'board', item_ids['board'])
    config.set('ItemIds', 'iu', item_ids['iu'])
    config.set('ItemIds', 'inu', item_ids['inu'])
    config.set('ItemIds', 'uu', item_ids['uu'])
    config.set('ItemIds', 'unu', item_ids['unu'])
    config.set('ItemIds', 'done', item_ids['done'])

    f = open(os.path.join(cfg_filepath, itemids_filename), 'w')
    config.write(f)
    f.close()

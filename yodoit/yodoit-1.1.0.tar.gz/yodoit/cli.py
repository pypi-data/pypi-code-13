"""YoDoit

Usage:
    yodoit
    yodoit <card-name> [--desc <desc>] (--iu | --inu | --uu | --unu | --done)
    yodoit -l [<list-names>...]
    yodoit -o
    yodoit --set-new-board
    yodoit --set-existing-board

Options:
    --iu    Use Important Urgent list.
    --inu   Use Important Not Urgent list.
    --uu    Use Unimportant Urgent list.
    --unu   Use Unimportant Not Urgent list.
    --done  Use Done list.
    --desc  Add a description to a card.
    -l      Show an ordered list of cards in all lists, or a specified list.
    -o      Open Trello Board in browser.
    --set-new-board
            Sets a new board for the CLI.
    --set-existing-board
            Sets an existing board for the CLI by using your Trello board ID.
"""

from docopt import docopt
import ConfigParser
import json
import requests
import webbrowser
import os
import sys


cfg_authkeys_filename = 'authkeys.cfg'
cfg_itemids_filename = 'itemids.cfg'
cfg_filepath = os.path.dirname(os.path.realpath(__file__))
api_url = "https://api.trello.com/1"


# Used to convert a list name to an abbreviated form for ease of use in CLI
list_name_convert = {
    "important urgent": "iu",
    "unimportant urgent": "uu",
    "important not urgent": "inu",
    "unimportant not urgent": "unu",
    "done": "done"
}


# Used to convert an abbreviated name to a list name
name_list_convert = {v: k for k, v in list_name_convert.items()}


def setup_auth():
    """ Sets up the CLI by creating a config file containing the user's Trello
    app key and auth token.
    :return:
    """
    print "Yo, welcome to YoDoIt!"
    auth_keys = {
        'app_key': '',
        'auth_token': ''
    }
    auth_keys['app_key'] = raw_input("Yo, enter your Trello app key: ")
    auth_keys['auth_token'] = raw_input("Yo, enter your Trello auth token: ")

    test_request = requests.get('%s/search?query=%s&key=%s&token=%s' % (api_url, 'yodoit_test_auth', auth_keys['app_key'], auth_keys['auth_token']))
    if test_request.status_code != requests.codes.ok:
        print "Invalid app key and/or auth token."
        sys.exit(1)
    else:
        create_cfg_authkeys_file(auth_keys)
        print "Yo, your Trello account is hooked up with YoDoIt!"


def setup_itemids(auth_args):
    """ Sets up the CLI by creating a config file containing the user's Trello
    board item IDs.
    :param auth_args:
    :return:
    """
    board_type = raw_input("Yo, do you wanna use a new board or an existing board? (new/existing): ")
    if board_type == 'new':
        setup_new_board(auth_args)
    elif board_type == 'existing':
        setup_existing_board(auth_args)
    else:
        print "Invalid input."
        sys.exit(1)


def setup_new_board(auth_args):
    item_ids = {
        'board': '',
        'iu': '',
        'inu': '',
        'uu': '',
        'unu': '',
        'done': '',
    }

    board_name = "YoDoIt"
    board_desc = "A simple decision making tool to help you be more productive."

    post_board_url = '%s/boards?name=%s&desc=%s&%s' % (api_url, board_name, board_desc, auth_args)
    request = requests.post(post_board_url)
    board = json.loads(request.text)

    item_ids['board'] = board['id']
    empty_new_board(auth_args, item_ids)
    add_yodoit_lists(auth_args, item_ids)
    create_cfg_itemids_file(item_ids)
    print "Yo, your new board is set!"


def setup_existing_board(auth_args):
    item_ids = {
        'board': '',
        'iu': '',
        'inu': '',
        'uu': '',
        'unu': '',
        'done': '',
    }

    print "Yo, go to your Trello board and get its board ID from the url\n" \
          "Example: trello.com/b/[board ID]/[board name]"
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

    validate_board_contents(item_ids)
    create_cfg_itemids_file(item_ids)
    print "Yo, your existing board is set!"


def validate_board_contents(item_ids):
    """ Checks if the board has the 4 Eisenhower Decision Matrix categories as
    lists and a Done list.
    :param item_ids:
    :return:
    """
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


def empty_new_board(auth_args, item_ids):
    """ Archives all lists in a board. Needed because when creating a board with
    Trello API, 3 default lists are created.
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
    """ Adds the 4 Eisenhower Decision Matrix categories + Done as lists to a
    board.
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


def create_cfg_authkeys_file(auth_keys):
    config = ConfigParser.ConfigParser()
    config.add_section('AuthKeys')
    config.set('AuthKeys', 'app_key', auth_keys['app_key'])
    config.set('AuthKeys', 'auth_token', auth_keys['auth_token'])

    f = open(os.path.join(cfg_filepath, cfg_authkeys_filename), 'w')
    config.write(f)
    f.close()


def create_cfg_itemids_file(item_ids):
    config = ConfigParser.ConfigParser()
    config.add_section('ItemIds')
    config.set('ItemIds', 'board', item_ids['board'])
    config.set('ItemIds', 'iu', item_ids['iu'])
    config.set('ItemIds', 'inu', item_ids['inu'])
    config.set('ItemIds', 'uu', item_ids['uu'])
    config.set('ItemIds', 'unu', item_ids['unu'])
    config.set('ItemIds', 'done', item_ids['done'])

    f = open(os.path.join(cfg_filepath, cfg_itemids_filename), 'w')
    config.write(f)
    f.close()


def add_card_to_list(auth_args, item_ids, list_name, card_name, card_desc):
    if card_desc is None:
        card_desc = ''

    post_api = '%s/lists/%s/cards?name=%s&desc=%s&due=%s&%s' % (api_url, item_ids[list_name], card_name, card_desc, 'null', auth_args)
    request = requests.post(post_api)

    if request.status_code == requests.codes.ok:
        print "Yo, do it!"
    else:
        print "Failed."


def list_cards(auth_args, item_ids, list_names):
    if not list_names:
        list_names = ['done', 'iu', 'inu', 'uu', 'unu']  # Enforces output order

    output = []

    for list_name in list_names:
        list_category = name_list_convert[list_name].title() + ":\n"
        get_api = '%s/lists/%s/cards?%s' % (api_url, item_ids[list_name], auth_args)
        request = requests.get(get_api)
        cards = json.loads(request.text)

        i = 1
        for card in cards:
            list_category += `i` + ". " + card['name'] + "\n"
            i += 1

        output.append(list_category)

    s = "\n"
    print s.join(output)


def main():
    args = docopt(__doc__)

    config = ConfigParser.ConfigParser()
    file_authkeys = config.read(os.path.join(cfg_filepath, cfg_authkeys_filename))
    if not file_authkeys:
        setup_auth()
        config.read(os.path.join(cfg_filepath, cfg_authkeys_filename))

    auth_args = 'key=%s&token=%s' % (config.get('AuthKeys', 'app_key'), config.get('AuthKeys', 'auth_token'))

    file_itemids = config.read(os.path.join(cfg_filepath, cfg_itemids_filename))
    if not file_itemids:
        setup_itemids(auth_args)
        config.read(os.path.join(cfg_filepath, cfg_itemids_filename))

    item_ids = {
        'board': config.get('ItemIds', 'board'),
        'iu': config.get('ItemIds', 'iu'),
        'inu': config.get('ItemIds', 'inu'),
        'uu': config.get('ItemIds', 'uu'),
        'unu': config.get('ItemIds', 'unu'),
        'done': config.get('ItemIds', 'done'),
    }

    if args['--iu']:
        add_card_to_list(auth_args, item_ids, 'iu', args['<card-name>'], args['<desc>'])
    elif args['--inu']:
        add_card_to_list(auth_args, item_ids, 'inu', args['<card-name>'], args['<desc>'])
    elif args['--uu']:
        add_card_to_list(auth_args, item_ids, 'uu', args['<card-name>'], args['<desc>'])
    elif args['--unu']:
        add_card_to_list(auth_args, item_ids, 'unu', args['<card-name>'], args['<desc>'])
    elif args['-l']:
        list_cards(auth_args, item_ids, args['<list-names>'])
    elif args['-o']:
        new = 2  # Try to open in new tab if browser already open
        url = "https://trello.com/b/%s" % item_ids['board']
        webbrowser.open(url, new)
    elif args['--set-new-board']:
        setup_new_board(auth_args)
    elif args['--set-existing-board']:
        setup_existing_board(auth_args)
    else:
        print "Yo, go to https://github.com/niketanpatel/yodoit-cli for usage."


if __name__ == '__main__':
    main()

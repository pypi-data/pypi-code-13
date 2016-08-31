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
from trello_api import api_url, name_list_convert
import yodoit_config
import json
import requests
import webbrowser


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

    auth_args = yodoit_config.get_auth_args()
    item_ids = yodoit_config.get_item_ids()

    if args['--iu']:
        add_card_to_list(auth_args, item_ids, 'iu', args['<card-name>'], args['<desc>'])
    elif args['--inu']:
        add_card_to_list(auth_args, item_ids, 'inu', args['<card-name>'], args['<desc>'])
    elif args['--uu']:
        add_card_to_list(auth_args, item_ids, 'uu', args['<card-name>'], args['<desc>'])
    elif args['--unu']:
        add_card_to_list(auth_args, item_ids, 'unu', args['<card-name>'], args['<desc>'])
    elif args['--done']:
        add_card_to_list(auth_args, item_ids, 'done', args['<card-name>'], args['<desc>'])
    elif args['-l']:
        list_cards(auth_args, item_ids, args['<list-names>'])
    elif args['-o']:
        url = "https://trello.com/b/%s" % item_ids['board']
        webbrowser.open(url, 2) # 2 is for trying to open in new tab
    elif args['--set-new-board']:
        yodoit_config.set_new_board(auth_args)
    elif args['--set-existing-board']:
        yodoit_config.set_existing_board(auth_args)
    else:
        print "Yo, use `yodoit -h` for usage."


if __name__ == '__main__':
    main()

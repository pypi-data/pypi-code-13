"""YoDoit

Usage:
    yodoit <card-name> [--desc <desc>] (--iu | --inu | --uu | --unu | --done)
    yodoit -l [<list-names>...]
    yodoit -o

Options:
    --iu    Use Important Urgent list.
    --inu   Use Important Not Urgent list.
    --uu    Use Unimportant Urgent list.
    --unu   Use Unimportant Not Urgent list.
    --done  Use Done list.
    --desc  Add a description to a card.
    -l      Show an ordered list of cards in all lists, or a specified list.
    -o      Open Trello Board in browser.

"""

from docopt import docopt
from trelloapi import API_URL, AUTH_PARAMS
import cfg_itemids as items
import getboardconfig
import json
import requests


item_ids = {
    'board': items.BOARD_ID,
    'iu': items.IU_ID,
    'inu': items.INU_ID,
    'uu': items.UU_ID,
    'unu': items.UNU_ID,
    'done': items.DONE_ID
}

name_list_convert = {v: k for k, v in getboardconfig.list_name_convert.items()}

def add_card_to_list(list_name, card_name, card_desc):
    if card_desc is None:
        card_desc = ''

    post_api = '%s/lists/%s/cards?name=%s&desc=%s&due=%s&%s' % (API_URL, item_ids[list_name], card_name, card_desc, 'null', AUTH_PARAMS)
    request = requests.post(post_api)

    if request.status_code == requests.codes.ok:
        print "Card \"" + card_name + "\" added to " + name_list_convert[list_name].title() + "."


def list_cards(list_names):
    if not list_names:
        list_names = ['done', 'iu', 'inu', 'uu', 'unu'] # Hard coded instead of using keys() on name_list_convert because it enforces order on output

    output = []

    for list_name in list_names:
        list_category = name_list_convert[list_name].title() + ":\n"
        get_api = '%s/lists/%s/cards?%s' % (API_URL, item_ids[list_name], AUTH_PARAMS)
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
    args = docopt(__doc__, version='1.0.0')

    if args['--iu']:
        add_card_to_list('iu', args['<card-name>'], args['<desc>'])
    elif args['--inu']:
        add_card_to_list('inu', args['<card-name>'], args['<desc>'])
    elif args['--uu']:
        add_card_to_list('uu', args['<card-name>'], args['<desc>'])
    elif args['--unu']:
        add_card_to_list('unu', args['<card-name>'], args['<desc>'])
    elif args['-l']:
        list_cards(args['<list-names>'])
    elif args['-o']:
        import webbrowser
        new = 2 # Open in new tab if browser already open
        url = "https://trello.com/b/%s" % item_ids['board']
        webbrowser.open(url, new)


if __name__ == '__main__':
    main()
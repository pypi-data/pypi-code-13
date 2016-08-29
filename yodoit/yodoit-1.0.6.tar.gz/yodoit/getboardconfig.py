from trelloapi import API_URL, AUTH_PARAMS
from cfg_authkeys import APP_KEY, AUTH_TOKEN
import requests
import json
import os.path
import sys

# Set of expected list names in an Eisenhower Decision Matrix
expected_list_names = set()
expected_list_names.add("important urgent")
expected_list_names.add("important not urgent")
expected_list_names.add("unimportant urgent")
expected_list_names.add("unimportant not urgent")
expected_list_names.add("done")

# Used to convert a list name to an abbreviated form for ease of use in CLI
list_name_convert = {
    "important urgent": "iu",
    "unimportant urgent": "uu",
    "important not urgent": "inu",
    "unimportant not urgent": "unu",
    "done": "done"
}

# Populated by getters to contain IDs for the lists in the Trello board
item_ids = {}


def set_existing_board_config():
    """ Creates a config file for an existing Trello board with the Eisenhower
    Decision Matrix categories. Populates the item_ids containing IDs for the
    items in the existing Trello board for external use.
    :return:
    """
    print "Go to your Trello board and get the board ID from the url\n" \
          "trello.com/b/[board ID]/[board name]"
    board_id = raw_input("Enter your Eisenhower Decision Matrix board ID: ")

    try:
        request = requests.get("%s/boards/%s/lists?%s" % (API_URL, board_id, AUTH_PARAMS))
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print e
        sys.exit(1)

    lists = json.loads(request.text)
    item_ids["board"] = lists[0]["idBoard"] # Uses long ID rather than shorthand

    for list in lists:
        if list["name"].lower() in expected_list_names:
            item_ids[list_name_convert[list["name"].lower()]] = list["id"]

    if len(item_ids) < 6: # 5 lists + board ID = 6
        print ("Invalid board. Your board must contain the following lists:"
               "\nImportant Urgent"
               "\nImportant Not Urgent"
               "\nUnimportant Urgent"
               "\nUnimportant Not Urgent"
               "\nDone")
        sys.exit(1)

    create_config_file()


def set_new_board_config():
    """ Creates a config file for a new Trello board with the Eisenhower
    Decision Matrix categories. Populates the item_ids containing IDs for the
    items in the new Trello board for external use.
    :return:
    """
    board_name = "Todo Matrix"
    board_desc = "A simple decision making tool"
    post_board_url = "%s/boards?name=%s&desc=%s&%s" % (API_URL, board_name, board_desc, AUTH_PARAMS)
    request = requests.post(post_board_url)

    response = json.loads(request.text)
    board_id = response["id"]
    item_ids["board"] = board_id
    empty_board(board_id)
    init_todo_matrix(board_id)
    create_config_file()


def empty_board(board_id):
    """ Archives all lists in a board.
    NOTE: When creating a board with Trello API, 3 default lists are created.
    However, when creating a board on the web app, default lists are not
    created. It's possible that this inconsistency is fixed in the future and
    thus this method won't be needed.
    :param board_id:
    :return:
    """
    get_lists_url = "%s/boards/%s/lists?%s" % (API_URL, board_id, AUTH_PARAMS)
    request = requests.get(get_lists_url)

    response = json.loads(request.text)
    for list in response:
        list_id = list["id"]
        put_list_url = "%s/lists/%s/closed?value=true&%s" % (API_URL, list_id, AUTH_PARAMS)
        requests.put(put_list_url)


def init_todo_matrix(board_id):
    """ Initializes the Todo Box board with the 4 Eisenhower Decision Matrix
    categories and a "Done" list
    :param board_id:
    :return:
    """
    done = requests.post("%s/boards/%s/lists?name=%s&%s" % (API_URL, board_id, "Done", AUTH_PARAMS))
    item_ids["done"] = json.loads(done.text)["id"]
    unu = requests.post("%s/boards/%s/lists?name=%s&%s" % (API_URL, board_id, "Unimportant Not Urgent", AUTH_PARAMS))
    item_ids["unu"] = json.loads(unu.text)["id"]
    uu = requests.post("%s/boards/%s/lists?name=%s&%s" % (API_URL, board_id, "Unimportant Urgent", AUTH_PARAMS))
    item_ids["uu"] = json.loads(uu.text)["id"]
    inu = requests.post("%s/boards/%s/lists?name=%s&%s" % (API_URL, board_id, "Important Not Urgent", AUTH_PARAMS))
    item_ids["inu"] = json.loads(inu.text)["id"]
    iu = requests.post("%s/boards/%s/lists?name=%s&%s" % (API_URL, board_id, "Important Urgent", AUTH_PARAMS))
    item_ids["iu"] = json.loads(iu.text)["id"]


def create_config_file():
    """ Takes all the list IDs and board ID from the item_ids and prints them
    out to a config file for use by the CLI script.
    :return:
    """
    configfile_name = "cfg_itemids.py"
    configfile_path = os.path.dirname(os.path.realpath(__file__))

    if os.path.isfile(os.path.join(configfile_path, configfile_name)):
        print "WARNING: This will rewrite your current Trello board's " \
              "configuration file."
        raw_input("Quit to stop the program or press Enter to continue...")

    ids = ("BOARD_ID = \"%s\""
           "\nIU_ID = \"%s\""
           "\nINU_ID = \"%s\""
           "\nUU_ID = \"%s\""
           "\nUNU_ID = \"%s\""
           "\nDONE_ID = \"%s\""
           % (item_ids["board"], item_ids["iu"], item_ids["inu"],
              item_ids["uu"], item_ids["unu"], item_ids["done"]))
    f = open(os.path.join(configfile_path, configfile_name), 'w')
    f.write(ids)
    print "Your Trello board is now hooked up to the CLI."


def create_auth_file():
    """ Creates a `cfg_authkeys.py` file by prompting the user for their Trello
    app key and auth token.
    :return:
    """
    if (APP_KEY != "") and (AUTH_TOKEN != ""):
        print "WARNING: This will rewrite the app key and auth token " \
              "already being used."
        raw_input("Quit to stop the program or press Enter to continue...")

    auth_filepath = os.path.dirname(os.path.realpath(__file__))

    app_key = raw_input("Enter your Trello app key: ")
    auth_token = raw_input("Enter your Trello auth token: ")
    authkeys = ("APP_KEY = \"%s\""
                "\nAUTH_TOKEN = \"%s\""
                % (app_key, auth_token))

    auth_filename = 'cfg_authkeys.py'
    f = open(os.path.join(auth_filepath, auth_filename), 'w')
    f.write(authkeys)

    print "Your Trello account is now hooked up to the CLI."

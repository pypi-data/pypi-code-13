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
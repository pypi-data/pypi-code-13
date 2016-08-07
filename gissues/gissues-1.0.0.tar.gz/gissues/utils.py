from datetime import datetime

#Splits items into equal number of items.
#Returns a list of those items (pages).
def paginate(items, items_per_page):
    return [items[i:i+items_per_page] for i in range(0, len(items), items_per_page)]

#Returns a string of [content] with [length] nubmer of characters.
def line(content, length=50):
    return(content * length + "\n")

#Prompts user if they want to confirm an action.
#Returns TRUE for 'yes' they DO want to continue.
#Returns FALSE for 'no' they DONT want to continue.
def confirm(action="modify"):
    confirm = input("Are you sure you want to {} this issue (Y/N): ".format(action.upper()))
    confirm = confirm.lower()

    if confirm == 'y' or confirm == 'yes':
        return True
    else:
        return False


def format_date(date):
    return datetime.strftime(date, "%m/%d/%y @ %H:%M")

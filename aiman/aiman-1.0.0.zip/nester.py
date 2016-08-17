"""
This is the nester.py module, and it provides one function called
withdraw_list which prints all the list that may or may not include nested list
"""

def withdraw_list(data):
    """This function takes positional argumaent called as list which is any
    python list. Each data item in the list provided is
    recursively printed to the screen on its own line"""
    for each_data in data:
        if isinstance(each_data,list):
            withdraw_list(each_data)
        else:
            print(each_data)

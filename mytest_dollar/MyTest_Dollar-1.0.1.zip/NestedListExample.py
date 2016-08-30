"""
This is sample function to iterate list of list of lists
"""
def printList(list_te):
    """
    Created a function named printList with an argument list_te 
    This iterates recursively 
    """    
    for each_item in list_te:
        if isinstance(each_item, list):
            printList(each_item)
        else:
            print(each_item)
            
             
# testList = ["one","two","three",["four","five",["six","seven"]]]
#  
# printList(testList)

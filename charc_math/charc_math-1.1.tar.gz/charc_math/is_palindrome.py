"""
    Checks if a number is plaindrome -- reads the same backwards
    @arg n  The number we check
    @ret    Boolean
"""

# Code:
def is_palindrome(n):
    """
    Checks if a number is plaindrome -- reads the same backwards
    @arg n  The number we check
    @ret    Boolean
    """
    return int(str(n)[::-1]) == n


# Bugs:

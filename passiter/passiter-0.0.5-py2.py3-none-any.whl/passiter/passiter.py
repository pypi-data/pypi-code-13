import random
from string import ascii_lowercase, ascii_uppercase, printable


def passiter(length=8, num_of_numbers=2, num_of_uppers=2, num_of_symbols=1):
    numbers = list(map(str, range(0, 10)))
    uppers = list(ascii_uppercase)
    lowers = list(ascii_lowercase)
    symbols = list(printable[62:94])  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    num_of_lowers = length - num_of_numbers - num_of_uppers - num_of_symbols
    while True:
        p = random.sample(numbers, num_of_numbers) + \
            random.sample(uppers, num_of_uppers) + \
            random.sample(lowers, num_of_lowers) + \
            random.sample(symbols, num_of_symbols)
        random.shuffle(p)
        yield ''.join(p)

if __name__ == '__main__':
    p = passiter()
    for _ in range(10):
        print(next(p))

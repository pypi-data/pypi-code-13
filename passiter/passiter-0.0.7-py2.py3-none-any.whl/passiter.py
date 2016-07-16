import random
from string import ascii_lowercase, ascii_uppercase, printable


def passiter(length=8, numbers=2, uppers=2, symbols=1):
    n = list(map(str, range(0, 10)))
    u = list(ascii_uppercase)
    l = list(ascii_lowercase)
    s = list(printable[62:94])  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    lowers = length - numbers - uppers - symbols
    while True:
        p = random.sample(n, numbers) + \
            random.sample(u, uppers) + \
            random.sample(l, lowers) + \
            random.sample(s, symbols)
        random.shuffle(p)
        yield ''.join(p)

if __name__ == '__main__':
    p = passiter()
    for _ in range(10):
        print(next(p))

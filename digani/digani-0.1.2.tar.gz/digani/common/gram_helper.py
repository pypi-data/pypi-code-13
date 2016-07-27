

def find_ngrams(string, n):
    input_list = string.split()
    return zip(*[input_list[i:] for i in range(n)])


def generate_strngram(string, n):
    return [' '.join(_) for _ in find_ngrams(string, n)]
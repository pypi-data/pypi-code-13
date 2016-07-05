from hashlib import sha1


def sha1_file(path):
    try:
        with open(path, 'rb') as f:
            return sha1(f.read()).hexdigest()
    except Exception:
        return sha1(bytes(5)).hexdigest()


def sha1_data(data):
    return sha1(data).hexdigest()

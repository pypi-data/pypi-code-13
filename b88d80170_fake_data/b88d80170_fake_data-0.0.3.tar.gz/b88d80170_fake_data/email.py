import hashlib


def email(first, last):
    f, l = first.lower(), last.lower()
    h = hashlib.new('md5')
    fn = f + l
    h.update(fn.lower().encode('utf-8'))
    digits = str(int('0x' + h.hexdigest(), 0))[0:3]
    return f[0] + l + digits + '@example.com'

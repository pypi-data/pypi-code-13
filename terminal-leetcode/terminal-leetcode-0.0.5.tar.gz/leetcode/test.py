
def enhance_code(func):
    def wrapper(*args, **kwargs):
        return 'before' + code + 'after' + language
        return func(*args, **kwargs)
    return wrapper


class Test(object):
    @enhance_code
    def test(self, *args, **kwargs):
        print self
        print 'hha'

print Test().test('haha', 'jasdf')

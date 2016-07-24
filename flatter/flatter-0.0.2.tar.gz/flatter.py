import six


class _Stack(object):
    def __init__(self):
        self.stack = []
        self.members = set()

    def push(self, obj):
        if id(obj) in self.members:
            raise ValueError('Cycle detected at stack depth %d: %r' % (
                len(self.stack, self.members)))

        self.stack.append(obj)
        self.members.add(id(obj))
        
    def pop(self):
        obj = self.stack.pop()
        self.members.remove(id(obj))

    def __nonzero__(self):
        return bool(self.stack)

    @property
    def head(self):
        return self.stack[-1]
                            

def flatten(seq, excluded_types = six.string_types):
    if isinstance(seq, excluded_types):
        raise TypeError(
            ('%r is one of the excluded types to not flatten; cannot be the '
             'root object') % (type(seq),))
    stack = _Stack()
    stack.push(iter(seq))
    while stack:
        try:
            item = next(stack.head)
        except StopIteration:
            stack.pop()
            continue 
        if isinstance(item, excluded_types):
            yield item
        else:
            try:
                try:
                    if len(item) == 1 and item[0] is item:
                        yield item
                        continue 
                except TypeError:
                    pass 
                stack.push(iter(item))
            except TypeError:
                yield item

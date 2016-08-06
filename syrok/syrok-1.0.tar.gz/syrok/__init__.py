import vk, time


class api:
    def __init__(self, user_token=''):
        self.token = user_token
        if user_token:
            self.user = vk.API(access_token=user_token, session=vk.Session(), v='5.52')
        else:
            self.user = vk.API(session=vk.Session(), v='5.52')
        self.last_call = time.time()
        self.calls = 0
        self.method = []

    def __call__(self, methods, **kwargs):
        while 1:
            if time.time()-self.last_call > 1:
                self.calls = 0
                self.last_call = time.time()
            if self.calls < 2:
                self.calls += 1
                r = self.user.__getattr__('.'.join(methods))(**kwargs)
                return r

    def __getattr__(self, item):
        return dummy(item, self)


class dummy:
    def __init__(self, method, parent):
        self.methods = [method]
        self.parent = parent

    def __getattr__(self, item):
        self.methods.append(item)
        return self

    def __call__(self, **kwargs):
        return self.parent.__call__(self.methods, **kwargs)
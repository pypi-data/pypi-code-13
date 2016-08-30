from urlparse import urlparse
from z3c.form import widget


def _wrap_update(update):
    def _wrapped(self):
        if hasattr(self.request, 'environ'):
            env = self.request.environ
            referrer = env.get('HTTP_REFERER', env.get('HTTP_REFERRER'))
            if referrer:
                req_url_parsed = urlparse(self.request.URL)
                referrer_parsed = urlparse(referrer)
                if req_url_parsed.netloc != referrer_parsed.netloc:
                    # We do not trust data from outside referrers.
                    self.ignoreRequest = True
            if (hasattr(self.form, 'method') and
                    self.request.REQUEST_METHOD.lower() != self.form.method.lower()):
                    # Unexpected request method.
                    self.ignoreRequest = True
        return update(self)
    return _wrapped


widget.Widget.update = _wrap_update(widget.Widget.update)

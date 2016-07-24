from flask.app import Flask
from schemagic.web import service_registry

app = Flask(__name__)
register_fibonacci_services = service_registry(app)

def memo(fn):
    _cache = {}
    def _f(*args, **kwargs):
        try:
            return _cache[(args, kwargs)]
        except KeyError:
            _cache[(args, kwargs)] = result = fn(*args, **kwargs)
            return result
        except TypeError:
            return fn(*args, **kwargs)
    _f.cache = _cache
    return _f

@memo
def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

# @app.route("/")
def home():
    return "Hello World"
app.add_url_rule(rule="/", view_func=home)
# app.add_url_rule(rule="/fib", view_func=)


register_fibonacci_services(
    dict(rule="/fibonacci",
         input_schema=int,
         output_schema=int,
         fn=fib))

if __name__ == '__main__':
    app.run(port=5000)
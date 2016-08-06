from .basket import Basket


def basket(request):
    if hasattr(request, 'session'):
        return {'basket': Basket(request.session)}
    return {}

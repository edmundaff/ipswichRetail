from .cart import Basket


def basket_count(request):
    return {'basket_count': Basket(request).count()}

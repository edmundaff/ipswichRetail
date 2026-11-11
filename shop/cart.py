from decimal import Decimal
from .models import Product

CART_SESSION_KEY = 'ipswich_basket'
MAX_PER_PRODUCT = 10


class Basket:
    """Session-backed basket. Money always comes from the database, never the browser."""

    def __init__(self, request):
        self.session = request.session
        self.data = self.session.get(CART_SESSION_KEY, {})
        if not isinstance(self.data, dict):
            self.data = {}

    def _save(self):
        self.session[CART_SESSION_KEY] = self.data
        self.session.modified = True

    def add(self, product, quantity=1):
        key = str(product.pk)
        old = int(self.data.get(key, 0))
        new = min(old + quantity, product.inventory, MAX_PER_PRODUCT)
        if new <= old:
            return False
        self.data[key] = new
        self._save()
        return True

    def update(self, product, quantity):
        key = str(product.pk)
        if quantity <= 0:
            self.data.pop(key, None)
        else:
            self.data[key] = min(quantity, product.inventory, MAX_PER_PRODUCT)
        self._save()

    def clear(self):
        self.data = {}
        self._save()

    def lines(self):
        keys = [int(k) for k in self.data if str(k).isdigit()]
        products = Product.objects.filter(pk__in=keys, is_active=True).select_related('category')
        rows = []
        for product in products:
            q = min(max(int(self.data.get(str(product.pk), 0)), 0), MAX_PER_PRODUCT)
            if q:
                rows.append({'product': product, 'quantity': q, 'line_total': product.price * q})
        return sorted(rows, key=lambda x: x['product'].name)

    def count(self):
        return sum(line['quantity'] for line in self.lines())

    def total(self):
        return sum((line['line_total'] for line in self.lines()), Decimal('0.00'))

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self, max_items):
        self.max_items = max_items
        self._items = []

    @property
    def items(self):
        return self._items.copy()

    def add_product(self, product):
        if len(self._items) < self.max_items:
            self._items.append(product)
        else:
            raise ValueError("Order limit reached")

    def total_cost(self):
        return sum(item.price for item in self._items)

    def item_count(self):
        return len(self._items)

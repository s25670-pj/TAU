import unittest
from order import Product, Order

class TestOrder(unittest.TestCase):
    
    def setUp(self):
        self.product1 = Product("Laptop", 3000)
        self.product2 = Product("Phone", 1500)
        self.product3 = Product("Headphones", 200)
        self.product4 = Product("Mouse", 50)
        self.order = Order(max_items=3)

    def test_add_product_within_limit(self):
        """Test adding a product within the item limit."""
        self.order.add_product(self.product1)
        self.assertEqual(self.order.item_count(), 1)

    def test_add_product_exceeds_limit(self):
        """Test adding a product when the limit is exceeded."""
        self.order.add_product(self.product1)
        self.order.add_product(self.product2)
        self.order.add_product(self.product3)
        with self.assertRaises(ValueError):
            self.order.add_product(self.product4)

    def test_add_product_at_limit(self):
        """Test adding a product exactly at the limit."""
        self.order.add_product(self.product1)
        self.order.add_product(self.product2)
        self.order.add_product(self.product3)
        self.assertEqual(self.order.item_count(), 3)

    def test_total_cost_single_product(self):
        """Test total cost calculation with a single product."""
        self.order.add_product(self.product1)
        self.assertEqual(self.order.total_cost(), 3000)

    def test_total_cost_multiple_products(self):
        """Test total cost calculation with multiple products."""
        self.order.add_product(self.product1)
        self.order.add_product(self.product2)
        self.order.add_product(self.product3)
        self.assertEqual(self.order.total_cost(), 4700)

    def test_total_cost_no_products(self):
        """Test total cost calculation with no products added."""
        self.assertEqual(self.order.total_cost(), 0)

    def test_item_count_no_products(self):
        """Test item count when no products are added."""
        self.assertEqual(self.order.item_count(), 0)

    def test_item_count_after_adding_products(self):
        """Test item count after adding multiple products."""
        self.order.add_product(self.product1)
        self.order.add_product(self.product2)
        self.assertEqual(self.order.item_count(), 2)

    def test_total_cost_type(self):
        """Test total cost result type is integer."""
        self.order.add_product(self.product1)
        self.order.add_product(self.product2)
        self.assertIsInstance(self.order.total_cost(), int)

    def test_product_list_not_mutable(self):
        """Test product list cannot be modified externally."""
        items = self.order.items
        items.append(self.product1)
        self.assertNotEqual(self.order.item_count(), len(items))

if __name__ == '__main__':
    unittest.main()

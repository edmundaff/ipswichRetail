from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from .models import Category, Order, OrderItem, Product


class RetailSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cat = Category.objects.create(name='Home & Living', slug='home-living')
        cls.tech = Category.objects.create(name='Tech', slug='tech')
        cls.mug = Product.objects.create(
            category=cls.cat, name='Slow Morning Mug', slug='slow-morning-mug',
            short_description='Cosy ceramics', description='A mug.', price=Decimal('16.50'),
            image_name='mug.svg', inventory=5, is_active=True, is_featured=True,
        )
        cls.headphones = Product.objects.create(
            category=cls.tech, name='Headphones', slug='headphones',
            short_description='Music', description='Listening.', price=Decimal('74.00'),
            image_name='headphones.svg', inventory=2, is_active=True,
        )

    def test_home_page(self):
        response = self.client.get(reverse('shop:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Everyday')
        self.assertContains(response, 'Slow Morning Mug')

    def test_catalogue_search_and_filter(self):
        response = self.client.get(reverse('shop:catalogue'), {'q': 'mug', 'category': 'home-living'})
        self.assertContains(response, 'Slow Morning Mug')
        self.assertNotContains(response, 'Headphones')

    def test_product_detail(self):
        response = self.client.get(reverse('shop:product_detail', args=['slow-morning-mug']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '£16.50')

    def test_add_and_update_basket(self):
        add = reverse('shop:basket_add', args=[self.mug.pk])
        self.assertEqual(self.client.post(add, {'quantity': '2'}).status_code, 302)
        self.assertContains(self.client.get(reverse('shop:basket')), '£33.00')
        update = reverse('shop:basket_update', args=[self.mug.pk])
        self.client.post(update, {'quantity': '1'})
        self.assertContains(self.client.get(reverse('shop:basket')), '£16.50')

    def test_reject_invalid_quantity(self):
        self.client.post(reverse('shop:basket_add', args=[self.mug.pk]), {'quantity': '999'})
        self.assertEqual(self.client.session.get('ipswich_basket', {}), {})

    def test_cannot_add_more_than_stock(self):
        self.client.post(reverse('shop:basket_add', args=[self.mug.pk]), {'quantity': '5'})
        self.client.post(reverse('shop:basket_add', args=[self.mug.pk]), {'quantity': '5'})
        self.assertEqual(self.client.session['ipswich_basket'][str(self.mug.pk)], 5)

    def test_checkout_creates_demo_order_and_decrements_stock(self):
        self.client.post(reverse('shop:basket_add', args=[self.mug.pk]), {'quantity': '2'})
        checkout = reverse('shop:demo_checkout')
        data = {'full_name': 'Test Shopper', 'email': 'test@example.com',
                'address_line': '1 Test Street', 'city': 'Ipswich', 'postcode': 'IP1 1AA'}

        self.assertRedirects(
            self.client.post(checkout, data),
            reverse('shop:basket'),
            fetch_redirect_response=False,
        )

        order = Order.objects.get()
        self.assertEqual(order.total, Decimal('33.00'))
        self.assertEqual(OrderItem.objects.get(order=order).quantity, 2)
        self.mug.refresh_from_db()
        self.assertEqual(self.mug.inventory, 3)
        self.assertEqual(self.client.session.get('ipswich_basket'), {})
        self.assertContains(self.client.get(reverse('shop:basket')), 'Demo order created!')

    def test_checkout_rejects_invalid_email(self):
        self.client.post(reverse('shop:basket_add', args=[self.mug.pk]), {'quantity': '1'})
        response = self.client.post(reverse('shop:demo_checkout'), {
            'full_name': 'Test Shopper', 'email': 'not-an-email',
            'address_line': '1 Test Street', 'city': 'Ipswich', 'postcode': 'IP1 1AA',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_checkout_rejects_empty_basket(self):
        response = self.client.post(reverse('shop:demo_checkout'), {})
        self.assertRedirects(response, reverse('shop:basket'))
        self.assertEqual(Order.objects.count(), 0)

    def test_get_cannot_change_basket(self):
        response = self.client.get(reverse('shop:basket_add', args=[self.mug.pk]))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(self.client.session.get('ipswich_basket', {}), {})

    def test_health_endpoint(self):
        response = self.client.get(reverse('shop:health'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ok', 'service': 'ipswich-retail-demo'})

from decimal import Decimal
from django.core.management.base import BaseCommand
from shop.models import Category, Product

CATEGORIES = [
    ('Home & Living', 'home-living', 'Everyday pieces that make home feel good.'),
    ('Tech', 'tech', 'Simple technology for everyday comfort.'),
    ('Accessories', 'accessories', 'Carry the good things with you.'),
    ('Stationery', 'stationery', 'Make space for ideas.'),
]
PRODUCTS = [
    dict(category='home-living', name='Amber Everyday Bottle', slug='amber-everyday-bottle', short_description='Your daily hydration, with a touch of warm colour.', description='A reusable amber-coloured bottle with a practical, clean silhouette. A simple everyday essential for your desk or kitchen.', price='18.00', image_name='bottle.svg', inventory=35, is_featured=True),
    dict(category='home-living', name='Soft Glow Desk Lamp', slug='soft-glow-desk-lamp', short_description='A gentle pool of light for creative evenings.', description='A compact desk lamp with a considered shape and an inviting finish. Designed to brighten working corners and late-night reading spots.', price='49.00', image_name='lamp.svg', inventory=20, is_featured=True),
    dict(category='home-living', name='Slow Morning Mug', slug='slow-morning-mug', short_description='A little ritual for your favourite hot drink.', description='A comfortable ceramic-style mug made for tea breaks, coffee moments and slowing down. A calm addition to your shelf.', price='16.50', image_name='mug.svg', inventory=42, is_featured=True),
    dict(category='accessories', name='The Daily Canvas Tote', slug='the-daily-canvas-tote', short_description='Room for the essentials and a little more.', description='A versatile canvas-style shopper with a simple illustrated design. Perfect for books, groceries and everything in between.', price='22.00', image_name='tote.svg', inventory=27, is_featured=True),
    dict(category='tech', name='Studio Wireless Headphones', slug='studio-wireless-headphones', short_description='Make your own space wherever you go.', description='Modern over-ear headphones designed with a clean look. This demonstration product showcases a tech category and stock handling.', price='74.00', image_name='headphones.svg', inventory=14, is_featured=False),
    dict(category='home-living', name='Cosy Knit Throw', slug='cosy-knit-throw', short_description='Soft textures for the moments that matter.', description='A warm textured throw in a timeless neutral shade, ideal for a sofa, reading chair or an extra layer of comfort.', price='39.00', image_name='throw.svg', inventory=12, is_featured=False),
    dict(category='stationery', name='The Daily Notes Set', slug='the-daily-notes-set', short_description='Where good ideas find their first home.', description='An elegant notebook and pencil combination for lists, sketches and big ideas. Designed to look right at home on a desk.', price='14.00', image_name='notebook.svg', inventory=33, is_featured=False),
    dict(category='stationery', name='Tidy Desk Organiser', slug='tidy-desk-organiser', short_description='A more considered home for your workspace.', description='A compact, compartmented desktop organiser for notes, pens and accessories. Keep the useful things close at hand.', price='28.00', image_name='organiser.svg', inventory=18, is_featured=False),
]


class Command(BaseCommand):
    help = 'Create the eight example products if missing (safe to run repeatedly).'

    def handle(self, *args, **options):
        cats = {}
        for name, slug, description in CATEGORIES:
            obj, _ = Category.objects.update_or_create(slug=slug, defaults={'name': name, 'description': description})
            cats[slug] = obj
        for product in PRODUCTS:
            obj = dict(product)
            slug = obj.pop('slug')
            obj['category'] = cats[obj['category']]
            obj['price'] = Decimal(obj['price'])
            Product.objects.get_or_create(slug=slug, defaults=obj)
        self.stdout.write(self.style.SUCCESS('Ensured 4 categories and up to 8 example products exist.'))

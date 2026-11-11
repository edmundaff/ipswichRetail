import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='Category', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=80, unique=True)),
            ('slug', models.SlugField(max_length=90, unique=True)),
            ('description', models.CharField(blank=True, max_length=200)),
        ], options={'ordering': ['name'], 'verbose_name_plural': 'categories'}),
        migrations.CreateModel(name='Product', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=140)),
            ('slug', models.SlugField(max_length=160, unique=True)),
            ('short_description', models.CharField(max_length=170)),
            ('description', models.TextField()),
            ('price', models.DecimalField(decimal_places=2, max_digits=8)),
            ('image_name', models.CharField(help_text='Filename in shop/static/shop/img/', max_length=100)),
            ('inventory', models.PositiveIntegerField(default=0)),
            ('is_active', models.BooleanField(default=True)),
            ('is_featured', models.BooleanField(default=False)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='shop.category')),
        ], options={'ordering': ['name']}),
        migrations.CreateModel(name='Order', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('reference', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ('full_name', models.CharField(max_length=100)),
            ('email', models.EmailField(max_length=254)),
            ('address_line', models.CharField(max_length=200)),
            ('city', models.CharField(max_length=100)),
            ('postcode', models.CharField(max_length=12)),
            ('total', models.DecimalField(decimal_places=2, max_digits=10)),
            ('status', models.CharField(default='demo', editable=False, max_length=30)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
        ], options={'ordering': ['-created_at']}),
        migrations.CreateModel(name='OrderItem', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('product_name', models.CharField(max_length=140)),
            ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
            ('quantity', models.PositiveIntegerField()),
            ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shop.order')),
            ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.product')),
        ]),
    ]

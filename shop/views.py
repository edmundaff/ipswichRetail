from decimal import Decimal
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .cart import Basket, MAX_PER_PRODUCT
from .forms import DemoCheckoutForm
from .models import Category, Product, Order, OrderItem


def home(request):
    return render(request, 'shop/home.html', {
        'featured': Product.objects.filter(is_active=True, is_featured=True).select_related('category')[:4],
        'categories': Category.objects.all(),
    })


def catalogue(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.all()
    query = request.GET.get('q', '').strip()[:100]
    category = request.GET.get('category', '').strip()[:90]
    order_by = request.GET.get('sort', 'featured')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(category__name__icontains=query))
    if category:
        products = products.filter(category__slug=category)
    if order_by == 'low':
        products = products.order_by('price', 'name')
    elif order_by == 'high':
        products = products.order_by('-price', 'name')
    else:
        products = products.order_by('-is_featured', 'name')
    return render(request, 'shop/catalogue.html', {
        'products': products, 'categories': categories, 'query': query,
        'selected_category': category, 'sort': order_by,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:3]
    return render(request, 'shop/product_detail.html', {'product': product, 'related': related})


@require_POST
def basket_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 0
    if quantity < 1 or quantity > MAX_PER_PRODUCT:
        messages.error(request, 'Choose a quantity between 1 and 10.')
    elif Basket(request).add(product, quantity):
        messages.success(request, f'{product.name} added to your basket.')
    else:
        messages.error(request, 'Sorry, no more of this item can be added.')
    return redirect('shop:basket')


@require_POST
def basket_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    try:
        quantity = int(request.POST.get('quantity', '0'))
    except (ValueError, TypeError):
        messages.error(request, 'Please enter a valid quantity.')
        return redirect('shop:basket')
    if quantity < 0 or quantity > MAX_PER_PRODUCT:
        messages.error(request, 'Quantity must be between 0 and 10.')
        return redirect('shop:basket')
    Basket(request).update(product, quantity)
    messages.success(request, 'Your basket has been updated.')
    return redirect('shop:basket')


def basket_view(request):
    basket = Basket(request)
    return render(request, 'shop/basket.html', {
        'lines': basket.lines(), 'total': basket.total(),
        'checkout_form': DemoCheckoutForm(), 'confirmation': request.session.pop('last_demo_order', None),
    })


@require_POST
def demo_checkout(request):
    basket = Basket(request)
    lines = basket.lines()
    form = DemoCheckoutForm(request.POST)
    if not lines:
        messages.error(request, 'Add a product before checking out.')
        return redirect('shop:basket')
    if not form.is_valid():
        return render(request, 'shop/basket.html', {
            'lines': lines, 'total': basket.total(), 'checkout_form': form,
        }, status=400)

    # All writes are one transaction; stock is decremented only for a valid demo order.
    with transaction.atomic():
        locked = {p.pk: p for p in Product.objects.select_for_update().filter(pk__in=[line['product'].pk for line in lines], is_active=True)}
        for line in lines:
            p = locked.get(line['product'].pk)
            if p is None or p.inventory < line['quantity']:
                messages.error(request, f"Insufficient stock for {line['product'].name}. Please update your basket.")
                return redirect('shop:basket')
        order = form.save(commit=False)
        order.total = sum((locked[line['product'].pk].price * line['quantity'] for line in lines), start=Decimal('0.00'))
        order.save()
        for line in lines:
            p = locked[line['product'].pk]
            OrderItem.objects.create(order=order, product=p, product_name=p.name, unit_price=p.price, quantity=line['quantity'])
            Product.objects.filter(pk=p.pk).update(inventory=F('inventory') - line['quantity'])

    basket.clear()
    request.session['last_demo_order'] = {'reference': order.short_reference, 'total': str(order.total)}
    return redirect('shop:basket')


def health(request):
    return JsonResponse({'status': 'ok', 'service': 'ipswich-retail-demo'})

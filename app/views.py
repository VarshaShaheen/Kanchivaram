from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Category
from django.http import HttpResponse
from django.contrib.auth.models import User


def index(request):
    images_with_prices = [
        {'src': 'app/img/pricecat/1.jpg', 'price_range': '1000-5000'},
        {'src': 'app/img/pricecat/2.jpg', 'price_range': '5001-10000'},
        {'src': 'app/img/pricecat/6.jpg', 'price_range': '20001-30000'},
        {'src': 'app/img/pricecat/4.jpg', 'price_range': '30001-40000'},
        {'src': 'app/img/pricecat/5.jpg', 'price_range': '40001-50000'},
        {'src': 'app/img/pricecat/6.jpg', 'price_range': '50001-60000'},
    ]
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'app/index.html', {
        'categories': categories,
        'products': products,
        'images_with_prices': images_with_prices
    })


def price_category(request, a, b):
    products_in_range = Product.objects.filter(mrp__gte=a, mrp__lte=b)
    return render(request, 'app/price_category/price_category.html', {'products': products_in_range})


def categories(request, category_slug):
    products = Product.objects.filter(category__slug=category_slug)
    return render(request, 'app/category/category.html', {'products': products})


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.mrp for item in cart_items)
    return render(request, 'app/cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product,
                                                        user=request.user)
    cart_item.save()
    return redirect('view_cart')


@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')


def product_detail(request, product_code):
    product = get_object_or_404(Product, code=product_code)
    return render(request, 'app/product/product.html', {'product': product})


def silk_care_instruction(request):
    return render(request, 'app/disclosure/silkcare.html')


def refund_and_return(request):
    return render(request, 'app/disclosure/refund.html')

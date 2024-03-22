from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Category
from django.http import HttpResponse
from django.contrib.auth.models import User


def index(request):
    price_categories = [
        {'src': 'app/img/pricecat/1.jpg', 'price_range': (1000, 5000)},
        {'src': 'app/img/pricecat/2.jpg', 'price_range': (5000, 10000)},
        {'src': 'app/img/pricecat/6.jpg', 'price_range': (20000, 30000)},
        {'src': 'app/img/pricecat/4.jpg', 'price_range': (30000, 40000)},
        {'src': 'app/img/pricecat/5.jpg', 'price_range': (40000, 50000)},
        {'src': 'app/img/pricecat/6.jpg', 'price_range': (50000, 60000)},

    ]

    images_kanchipuram = [
        {'src': 'app/img/kanchipuram/1.jpg', 'name': 'Pure Tissue Kanchipuram Silk'},
        {'src': 'app/img/kanchipuram/2.jpg', 'name': 'Pure Organza Tissue Silk'},
        {'src': 'app/img/kanchipuram/3.jpg', 'name': 'Pure Kanchipuram Silk'},
        {'src': 'app/img/kanchipuram/4.jpg', 'name': 'Pure Designer Kanchipuram Silk'},
        {'src': 'app/img/kanchipuram/5.jpg', 'name': 'Korvai Kanchipuram Silk'},
        {'src': 'app/img/kanchipuram/6.jpg', 'name': 'Pure Kanchipuram Soft Silk'},
    ]

    images_occasional = [
        {'src': 'app/img/occasional/1.jpg', 'name': 'Pure Tussac Silk'},
        {'src': 'app/img/occasional/2.jpg', 'name': 'Pure Matka Silk '},
        {'src': 'app/img/occasional/3.jpg', 'name': 'Pure Organza Silk'},
        {'src': 'app/img/occasional/4.jpg', 'name': 'Jute Silk'},
        {'src': 'app/img/occasional/5.jpg', 'name': 'Modal Silk'},
    ]

    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'app/index.html', {
        'categories': categories,
        'products': products,
        'price_categories': price_categories,
        'images_kanchipuram': images_kanchipuram,
        'images_occasional': images_occasional
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


def about_us(request):
    return render(request, 'app/about/about.html')


def contact_us(request):
    return render(request, 'app/contact/contact.html')

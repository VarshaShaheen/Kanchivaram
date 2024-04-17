from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem
from django.http import JsonResponse


def index(request):
    return render(request, 'app/index.html')


def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.mrp for item in cart_items)
    return render(request, 'app/cart/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def product_detail(request, product_code):
    product = get_object_or_404(Product, code=product_code)
    similar_products = Product.objects.all()
    return render(request, 'app/product/product.html', {'product': product, 'similar_products': similar_products})


def silk_care_instruction(request):
    return render(request, 'app/disclosure/silkcare.html')


def refund_and_return(request):
    return render(request, 'app/disclosure/refund.html')


def about_us(request):
    return render(request, 'app/about/about.html')


def contact_us(request):
    return render(request, 'app/contact/contact.html')


def terms_and_conditions(request):
    return render(request, 'app/disclosure/terms.html')


def shipping_and_delivery(request):
    return render(request, 'app/disclosure/shipping_and_delivery.html')


def privacy_policy(request):
    return render(request, 'app/disclosure/privacy_policy.html')


def disclaimer_policy(request):
    return render(request, 'app/disclosure/disclaimer.html')


def return_policy(request):
    return render(request, 'app/disclosure/return.html')


def catalogue(request):
    products = Product.objects.all()
    return render(request, 'app/catalogue/catalogue.html', {'products': products})


@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        return JsonResponse({'success': False, 'message': 'Product out of stock'})
    else:
        cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
        if created:
            return JsonResponse({'success': True, 'message': 'Product added to cart'})
        else:
            return JsonResponse({'success': False, 'message': 'Product already in cart'})


@login_required(login_url='/login/')
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

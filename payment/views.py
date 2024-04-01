import hashlib
import threading
from hmac import compare_digest
import logging

from django.conf import settings
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from app.models import CartItem
# from .models import send_email
from .models import Payment
from app.models import Order

logger = logging.getLogger("payment")


def verify_payment(data, token):
    logger.info("Verifying payment")
    generated_token = generate_token_from_dict(data, settings.PAYMENT_KEY)
    return compare_digest(generated_token, token)


def hash_str(data):
    hashing_algorithm = hashlib.sha512
    print(f"{data=}")
    hashed_data = hashing_algorithm(data.encode()).hexdigest()
    return hashed_data


def generate_token_from_dict(consumer_data, salt):
    data_to_hash = "|".join(str(value) for value in consumer_data) + "|" + salt
    return hash_str(data_to_hash)


class PaymentView(TemplateView):
    template_name = "app/checkout/checkout.html"

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.mrp for item in cart_items)
        return render(request, self.template_name, {'cart_items': cart_items, 'total_price': total_price})
    
    def post(self, request, *args, **kwargs):
        out_of_stock = False
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                if item.product.stock == 0 :
                    messages.error(request, f'Product {item.product} is out of stock')
                    out_of_stock = True
            if out_of_stock:
                return redirect('/catalogue/')
            else:
                items_total = cart_items.aggregate(Sum('product__mrp'))['product__mrp__sum'] or 0
                shipping_cost = 0
                total_amount = items_total + shipping_cost

                logger.debug(f"Payment creation request {request.POST}")

                # Create payment with the calculated total amount
                payment = Payment.objects.create(
                    amount=total_amount,  # Use the calculated total amount here
                    currency="INR",
                    user=request.user,
                )                
                for item in cart_items:
                    payment.cart_items.add(item)
                
                consumer_data = {
                    'merchant_id': 'L998462',
                    'txn_id': payment.id,
                    'total_amount': total_amount,
                    'account_no': '',
                    'consumer_id': '',
                    'consumer_mobile_no': '',
                    'consumer_email_id': '',
                    'debit_start_date': '',
                    'debit_end_date': '',
                    'max_amount': '',
                    'amount_type': '',
                    'frequency': '',
                    'card_number': '',
                    'exp_month': '',
                    'exp_year': '',
                    'cvv_code': '',
                }
                logger.info(f"{consumer_data = }")

                salt = settings.PAYMENT_KEY

                generated_token = generate_token_from_dict(list(consumer_data.values()), salt)
                logger.info(f"{generated_token=}")
                return render(request, "payment/confirm_payment.html",
                            {'token': generated_token, 'consumer_data': consumer_data,
                            "payment": payment, "currency": "INR"})
        else:
            return redirect('#')

@csrf_exempt
def payment_verification(request):
    # Extract necessary information from the request
    payment_data = request.POST
    t_data = payment_data["msg"].split("|")
    txn_id = t_data[3]
    txn_status = t_data[1]
    print(txn_status)
    token = t_data.pop()
    logger.debug("payment webhook called")
    logger.debug(f"{t_data =}")
    if verify_payment(t_data, token):
        payment = Payment.objects.filter(id=txn_id)
        if not payment.exists():
            logger.error("payment not found for transaction {}".format(txn_id))
            return JsonResponse({'status': 'failure'})
        payment = payment.first()
        for item in payment.cart_items.all():
            item.product.stock -= 1
            item.product.save()
        print("payment found")
        print(t_data[1])
        if txn_status == 'SUCCESS':
            logger.debug("payment verified and got success {}".format(txn_id))
            payment.status = 'success'
            payment.save()
            Order.objects.create(user=payment.user, payment=payment)
            # sendmail(
            #     f"Dear sir, "
            #     f"You have been successfully registered for the participation of MARICON-2024.",payment.user.email,"Maricon Registration Fee Payment"
            # )
        else:
            logger.error("payment verified and got failed {}".format(txn_id))
            payment.status = 'failed'
            payment.save()
            for item in payment.cart_items.all():
                item.product.stock += 1
                item.product.save()
            # sendmail(
            #     f"Dear sir, "
            #     f"Your payment has failed and transaction id  is {txn_id} please retry  the payment or contact the team to complete the registration process"
            #     "with Regards \n Maricon",payment.user.email,"Maricon Registration Fee")

            return redirect('/checkout/?error=payment_failed')
        return redirect('/maricon/abstract/?payment=success')
    else:
        logger.error("payment verification failed {}".format(txn_id))
        return JsonResponse({'status': 'failure'})


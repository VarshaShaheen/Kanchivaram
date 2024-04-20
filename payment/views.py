import hashlib
from hmac import compare_digest
import logging
import os

from django.conf import settings
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib import messages

from app.models import CartItem
from .models import Address, send_email
from .models import Payment
from app.models import Order

from twilio.rest import Client


logger = logging.getLogger("payment")

# ACCOUNT_SID = settings.ACCOUNT_SID
# AUTH_TOKEN = settings.AUTH_TOKEN
# client = Client(ACCOUNT_SID, AUTH_TOKEN)



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
    country_charges = {
        "AFGHANISTAN (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
        "ARGENTINA (FED)": {"charge_1kg": 4100, "charge_additional_500g": 600},
        "AUSTRALIA (DTDC)": {"charge_1kg": 2600, "charge_additional_500g": 500},
        "AUSTRIA (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "ARMENIA (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "AZERBAIJAN (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
        "BAHRAIN (DTDC)": {"charge_1kg": 2700, "charge_additional_500g": 500},
        "BELGIUM (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "BANGLADESH (DTDC)": {"charge_1kg": 2300, "charge_additional_500g": 500},
        "BRAZIL (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
        "CAMBODIA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
        "CAMEROON (FED)": {"charge_1kg": 4100, "charge_additional_500g": 800},
        "CANADA (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "CHILE (FED)": {"charge_1kg": 4100, "charge_additional_500g": 600},
        "CHINA (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "COLOMBIA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
        "COSTA RICA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
        "CROATIA (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
        "CZECH REP (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
        "DENMARK (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "EGYPT (FED)": {"charge_1kg": 3700, "charge_additional_500g": 500},
        "ETHOPIA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
        "FINLAND (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
        "FRANCE (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
        "GEORGIA (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
        "GERMANY (FED)": {"charge_1kg": 4000, "charge_additional_500g": 600},
        "GHANA (FED)": {"charge_1kg": 4100, "charge_additional_500g": 600},
        "GREECE (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "HONG KONG (FED)": {"charge_1kg": 3700, "charge_additional_500g": 700},
        "HUNGARY (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "ICELAND (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
        "INDIA (IND)": {"charge_1kg": 0, "charge_additional_500g": 0},
        "INDONESIA (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
        "IRAN (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
        "IRAQ (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "IRELAND (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "ISRAEL (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
        "ITALY (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "JAMAICA (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
        "JAPAN (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "JORDAN (FED)": {"charge_1kg": 3700, "charge_additional_500g": 600},
        "KAZAKHSTAN (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "KENYA (FED)": {"charge_1kg": 4100, "charge_additional_500g": 700},
        "KUWAIT (DTDC)": {"charge_1kg": 2700, "charge_additional_500g": 500},
        "LATVIA (FED)": {"charge_1kg": 4000, "charge_additional_500g": 600},
        "LEBANON (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "LIBIYA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
        "LUXEMBOURG (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "MALAYSIA (DTDC)": {"charge_1kg": 2100, "charge_additional_500g": 500},
        "MALDIVES (DTDC)": {"charge_1kg": 2200, "charge_additional_500g": 600},
        "MALTA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
        "MEXICO (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
        "MOROCCO (FED)": {"charge_1kg": 4100, "charge_additional_500g": 700},
        "MYANMAR (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
        "NEPAL (DTDC)": {"charge_1kg": 2000, "charge_additional_500g": 600},
        "NETHERLANDS (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
        "NEW ZEALAND (FED)": {"charge_1kg": 4000, "charge_additional_500g": 600},
        "NIGERIA (FED)": {"charge_1kg": 4100, "charge_additional_500g": 800},
        "NORWAY (FED)": {"charge_1kg": 3800, "charge_additional_500g": 700},
        "OMAN (DTDC)": {"charge_1kg": 2700, "charge_additional_500g": 500},
        "PANAMA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 800},
        "PERU (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
        "PHILIPPINES (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "POLAND (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
        "PORTUGAL (FED)": {"charge_1kg": 3900, "charge_additional_500g": 600},
        "QATAR (DTDC)": {"charge_1kg": 2700, "charge_additional_500g": 600},
        "SAUDI (DTDC)": {"charge_1kg": 2200, "charge_additional_500g": 500},
        "SERBIA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
        "SINGAPORE (DTDC)": {"charge_1kg": 2000, "charge_additional_500g": 500},
        "SLOVAKIA (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
        "SOUTH AFRICA (FED)": {"charge_1kg": 4000, "charge_additional_500g": 700},
        "SPAIN (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "SRILANKA (DTDC)": {"charge_1kg": 2500, "charge_additional_500g": 500},
        "SWEDAN (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "SWITZERLAND (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
        "TAIWAN (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "THAILAND (DTDC)": {"charge_1kg": 2300, "charge_additional_500g": 600},
        "TURKEY (FED)": {"charge_1kg": 3700, "charge_additional_500g": 700},
        "UAE (DTDC)": {"charge_1kg": 2200, "charge_additional_500g": 500},
        "UK (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "USA (DTDC)": {"charge_1kg": 3200, "charge_additional_500g": 600},
        "URUGUAY (FED)": {"charge_1kg": 3800, "charge_additional_500g": 600},
        "YEMEN (FED)": {"charge_1kg": 3900, "charge_additional_500g": 700},
        "ZIMBAWE (FED)": {"charge_1kg": 4100, "charge_additional_500g": 800},
    }

    state_charges = {
        "KERALA": {
            "kg_rate_normal": 0,
            "kg_rate_speed": 290,
            "add_500_speed": 70,
            "add_500_normal": 35
        },
        "TAMIL NADU": {
            "kg_rate_normal": 90,
            "kg_rate_speed": 350,
            "add_500_speed": 100,
            "add_500_normal": 50
        },
        "KARNATAKA": {
            "kg_rate_normal": 90,
            "kg_rate_speed": 350,
            "add_500_speed": 100,
            "add_500_normal": 50
        },
        "ANDHRA PRADESH": {
            "kg_rate_normal": 90,
            "kg_rate_speed": 350,
            "add_500_speed": 100,
            "add_500_normal": 50
        },
        "TELANGANA": {
            "kg_rate_normal": 90,
            "kg_rate_speed": 350,
            "add_500_speed": 100,
            "add_500_normal": 50
        },
        "GOA": {
            "kg_rate_normal": 100,
            "kg_rate_speed": 350,
            "add_500_speed": 100,
            "add_500_normal": 50
        },
        "MAHARASHTRA": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "GUJARAT": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "RAJASTHAN": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "PUNJAB": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "HARYANA": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "UTTAR PRADESH": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "MADHYA PRADESH": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "WEST BENGAL": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "BIHAR": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "JHARKHAND": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "ODISHA": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "CHHATTISGARH": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "UTTARAKHAND": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "HIMACHAL PRADESH": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "JAMMU AND KASHMIR": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "ASSAM": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "MEGHALAYA": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "TRIPURA": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "MIZORAM": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "MANIPUR": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "NAGALAND": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "ARUNACHAL PRADESH": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
        "SIKKIM": {
            "kg_rate_normal": 200,
            "kg_rate_speed": 500,
            "add_500_speed": 190,
            "add_500_normal": 95
        },
    }

    template_name = "app/checkout/checkout.html"

    def calculate_delivery_charge(self, country, state, total_weight, speed_delivery=False):
        charge_additional_500g = 0
        charge_1kg = 0
        if country == "INDIA (IND)":
            state_charge = self.state_charges.get(state)
            if state_charge:
                if speed_delivery:
                    charge_1kg = state_charge["kg_rate_speed"]
                    charge_additional_500g = state_charge["add_500_speed"]
                else:
                    charge_1kg = state_charge["kg_rate_normal"]
                    charge_additional_500g = state_charge["add_500_normal"]
        else:
            country_charge = self.country_charges.get(country)
            if country_charge:
                charge_1kg = country_charge["charge_1kg"]
                charge_additional_500g = country_charge["charge_additional_500g"]
            else:
                return None  # Country not found

        # Calculate the total charge based on weight
        if total_weight > 1000:
            extra_weight = total_weight - 1000
            extra_charge_units = (extra_weight + 499) // 500
            extra_charge = extra_charge_units * charge_additional_500g
            total_charge = charge_1kg + extra_charge
        else:
            total_charge = charge_1kg

        return total_charge

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.mrp for item in cart_items)
        total_weight = sum(item.product.weight for item in cart_items)
        country_charges = self.country_charges
        countries = country_charges.keys()
        states = self.state_charges.keys()
        return render(request, self.template_name,
                      {'cart_items': cart_items, 'total_price': total_price, 'countries': countries,
                       'total_weight': total_weight, 'states': states})

    def post(self, request, *args, **kwargs):
        out_of_stock = False
        print(f"{request.POST = }")
        if request.user.is_authenticated:
            Address.objects.create(
                user=request.user,
                first_name=request.POST.get('firstname'),  # Adjusted to match the keys in request.POST
                last_name=request.POST.get('lastname'),  # Adjusted to match the keys in request.POST
                address_line_1=request.POST.get('address1'),  # Adjusted to match the keys in request.POST
                address_line_2=request.POST.get('address2'),  # Adjusted to match the keys in request.POST
                state=request.POST.get('state'),  # Assuming 'state' contains the state name
                pincode=request.POST.get('zipcode'),  # Adjusted to match the keys in request.POST
                phone_number=request.POST.get('phone'),  # Adjusted to match the keys in request.POST
                email=request.POST.get('email'),
                country=request.POST.get('country'),
            )
            selected_country = request.POST.get('country')
            selected_state = request.POST.get('state')
            cart_items = CartItem.objects.filter(user=request.user)
            total_weight = sum(item.product.weight for item in cart_items)
            speed_delivery = request.POST.get('speed_delivery') == 'on'
            shipping_charge = self.calculate_delivery_charge(selected_country, selected_state, total_weight,
                                                             speed_delivery)
            for item in cart_items:
                if item.product.stock <= 0:
                    messages.error(request, f'Product {item.product} is out of stock')
                    out_of_stock = True
            if out_of_stock:
                return redirect('/catalogue/')
            else:
                items_total = cart_items.aggregate(Sum('product__mrp'))['product__mrp__sum'] or 0
                total_amount = items_total + shipping_charge

                logger.debug(f"Payment creation request {request.POST}")
                payment = Payment.objects.create(
                    amount=total_amount,
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
                return render(request, "payment/confirm_payment.html", {
                    'token': generated_token,
                    'consumer_data': consumer_data,
                    "payment": payment,
                    "currency": "INR",
                    "shipping_charge": shipping_charge,
                })

        else:
            return redirect('#')


@csrf_exempt
def payment_verification(request):
    if request.method == 'POST':
        payment_data = request.POST
        t_data = payment_data["msg"].split("|")
        txn_id = t_data[3]
        # txn_status = t_data[1]
        txn_status = "SUCCESS"
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
            print("payment found")
            print(t_data[1])
            if txn_status == 'SUCCESS':
                logger.debug("payment verified and got success {}".format(txn_id))
                payment.status = 'success'
                payment.save()
                cart_items = CartItem.objects.filter(user=payment.user)
                product_details = ""
                for item in cart_items:
                    # Add product IDs to the string
                    product_details += str(item.product.id) + ','

                # Remove the trailing comma
                product_details = product_details.rstrip(',')

                product_details = product_details
                address = Address.objects.filter(user=payment.user).last()
                order = Order.objects.create(user=payment.user, payment=payment,address=address,product_details=product_details)
                for item in cart_items:
                    item.delete()
                send_email( f"Dear customer, your order has been placed successfully.",payment.user.email,"Order "
                                                                                                            "placed "
                                                                                                            "successfully" )
                # send_whatsapp_message(request,order)
                
            else:
                logger.error("payment verified and got failed {}".format(txn_id))
                payment.status = 'failed'
                payment.save()
                for item in payment.cart_items.all():
                    item.product.stock += 1
                    item.product.save()
                send_email(f"Dear customer, your payment has been failed.", payment.user.email, "Payment failed")
                return render(request, 'payment/failure.html',
                                {'status': payment.status, 'txn_id': txn_id, 'txn_status': txn_status})
                # return JsonResponse({'status': 'failure'
                #                      ,'txn_id': txn_id,
                #                      'txn_status': txn_status})
            return render(request, 'payment/success.html', {
                'status': payment.status,
                'order_id': order.id,
                'payment_id': payment.id,
                'amount': payment.amount,
                'currency': payment.currency,
                'txn_id': txn_id,
                'txn_status': txn_status})
        else:
            payment = Payment.objects.filter(id=txn_id).first()
            payment.status = 'failed'
            for item in payment.cart_items.all():
                item.product.stock += 1
                item.product.save()
            payment.save()
            logger.error("payment verification failed {}".format(txn_id))
            send_email(f"Dear customer, your payment has been failed.", payment.user.email, "Payment failed")
            return render(request, 'payment/failure.html',
                          {'status': payment.status, 'txn_id': txn_id, 'txn_status': txn_status})
    else:
        return JsonResponse({'status': 'why are you here? you cant be here!'})


# def send_whatsapp_message(request,order):
#     order_data = {
#     "user": {
#         "name": order.user,
#         "email": order.user.email,
#     },
#     "payment": {
#         "amount": order.payment.amount,
#         "currency": order.payment.currency,
#     },
#     "status": order.status,
#     "address": {
#         "first_name": order.address.first_name,
#         "last_name": order.address.last_name,
#         "address_line_1": order.address.address_line_1,
#         "address_line_2": order.address.address_line_2,
#         "state": order.address.state,
#         "pincode": order.address.pincode,
#         "phone_number": order.address.phone_number,
#         "email": order.address.email,
#         "country": order.address.country,
#     },
#     "tracking_id": order.tracking_id if order.tracking_id else "N/A",
#     "products": []
#     }

#     # Include details of each product in the cart
#     for cart_item in order.payment.cart_items.all():
#         product_data = {
#             "name": cart_item.product.name,
#             "code": cart_item.product.code
#         }
#         order_data["products"].append(product_data)
#         print(f'{order_data}')
#     message = client.messages.create(
#                               body=f'{order_data}',
#                               from_='+15017122661',
#                               to='+15558675310'
#                           )

#     print(message.sid)

@csrf_exempt
def reduce_stock(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            item.product.stock -= 1
            item.product.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})

import hashlib
from hmac import compare_digest
import logging

from django.conf import settings
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib import messages

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

    template_name = "app/checkout/checkout.html"

    def calculate_delivery_charge(self, country, total_weight):
        country_charge = self.country_charges.get(country)
        if country_charge:
            charge_1kg = country_charge["charge_1kg"]
            charge_additional_500g = country_charge["charge_additional_500g"]

            rounded_weight = ((total_weight - 1000) // 500 + 1) * 500

            total_charge = charge_1kg + (rounded_weight // 500) * charge_additional_500g
            return total_charge
        else:
            return None

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.mrp for item in cart_items)
        total_weight = sum(item.product.weight for item in cart_items)
        country_charges = self.country_charges
        countries = country_charges.keys()
        return render(request, self.template_name,
                      {'cart_items': cart_items, 'total_price': total_price, 'countries': countries,
                       'total_weight': total_weight})

    def post(self, request, *args, **kwargs):
        out_of_stock = False
        if request.user.is_authenticated:
            selected_country = request.POST.get('country')
            cart_items = CartItem.objects.filter(user=request.user)
            total_weight = sum(item.product.weight for item in cart_items)
            shipping_charge = self.calculate_delivery_charge(selected_country, total_weight)
            for item in cart_items:
                if item.product.stock == 0:
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
                order = Order.objects.create(user=payment.user, payment=payment)
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
            payment.save()
            logger.error("payment verification failed {}".format(txn_id))
            return render(request, 'payment/failure.html',
                          {'status': payment.status, 'txn_id': txn_id, 'txn_status': txn_status})
    else:
        return JsonResponse({'status': 'why are you here? you cant be here!'})

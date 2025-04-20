# payment/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import Payment, Transactions
from garbage.models import Garbage
from user.models import Users

import razorpay
from decouple import config
import datetime

from django.views.generic import ListView, DetailView
from .models import Payment, Transactions
from user.models import Users
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Payment

class RazorpayView(View):
    def get(self, request, uuid):
        user = Users.objects.get(profile=request.user)
        garbage = get_object_or_404(Garbage, uuid=uuid, customer=user)
        payment = get_object_or_404(Payment, garbage=garbage)

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))
        receipt_id = f"receipt_{str(garbage.uuid)[:32]}"
        data = {
            "amount": int(payment.amount * 100),
            "currency": "INR",
            "receipt": receipt_id
        }

        rzp_order = client.order.create(data=data)
        order_id = rzp_order['id']

        Transactions.objects.create(
            payment=payment,
            rzp_order_id=order_id,
            amount=payment.amount
        )

        return render(request, 'payments/razorpay-page.html', {
            'order_id': order_id,
            'amount': data['amount'],
            'RZP_CLIENT_ID': config('RZP_CLIENT_ID'),
            'uuid': uuid
        })

@method_decorator(csrf_exempt, name='dispatch')
class PaymentVerify(View):
    def post(self, request):
        data = request.POST
        rzp_order_id = data.get('razorpay_order_id')
        rzp_payment_id = data.get('razorpay_payment_id')
        rzp_signature = data.get('razorpay_signature')

        transaction = get_object_or_404(Transactions, rzp_order_id=rzp_order_id)
        transaction.rzp_payment_id = rzp_payment_id
        transaction.rzp_signature = rzp_signature

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': rzp_order_id,
                'razorpay_payment_id': rzp_payment_id,
                'razorpay_signature': rzp_signature
            })

            transaction.status = 'Success'
            transaction.transaction_at = datetime.datetime.now()

            payment = transaction.payment
            payment.status = 'Success'
            payment.paid_at = datetime.datetime.now()
            payment.save()

            transaction.save()

            return redirect('payment-details', uuid=payment.garbage.uuid)

        except razorpay.errors.SignatureVerificationError:
            transaction.status = 'Failed'
            transaction.transaction_at = datetime.datetime.now()
            transaction.save()

            return redirect('payment-details', uuid=transaction.payment.garbage.uuid)

class PaymentDetailView(View):
    def get(self, request, uuid):

        if request.user.is_superuser:  # Check if the user is an admin
            # Admin can view payment details for any garbage entry
            garbage = get_object_or_404(Garbage, uuid=uuid)
            payment = get_object_or_404(Payment, garbage=garbage)
            
        else:
            user = Users.objects.get(profile=request.user)
            garbage = get_object_or_404(Garbage, uuid=uuid, customer=user)
            payment = get_object_or_404(Payment, garbage=garbage)
           
           
        transaction = Transactions.objects.filter(payment=payment).first()

        return render(request, 'payments/payment-details.html', {
                'payment': payment,
                'transaction': transaction,
        })
    

class PaymentListView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:  # Check if user is admin
            payments = Payment.objects.all()
        else:
            user = Users.objects.get(profile=request.user)
            payments = Payment.objects.filter(customer=user)  # Regular user can only see their payments

        return render(request, 'payments/payment_list.html', {'payments': payments})

# @method_decorator(login_required, name='dispatch')
# class PaymentDetail(View):
#     def get(self, request, uuid, *args, **kwargs):
#         payment = get_object_or_404(Payment, garbage__uuid=uuid)


#         transaction = Transactions.objects.filter(payment=payment).last()
#         context = {
#             'payment': payment,
#             'transaction': transaction
#         }
#         return render(request, 'payments/payment-details.html', context)
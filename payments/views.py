from django.shortcuts import render,redirect,get_object_or_404

from django.views import View

from .models import Payment,Transactions

import razorpay

from decouple import config

from django.db import transaction

# csrf_exempt

from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

import datetime 

from pet_app . models import Pets

from customer . models import Customer

from django.contrib.auth.decorators import login_required

class RazorpayView(View):

    def get(self, request, uuid, *args, **kwargs):

        customer = Customer.objects.get(profile=request.user)

        pet = get_object_or_404(Pets, uuid=uuid, customer=customer)

        payment = get_object_or_404(Payment, pet=pet)

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))

        receipt_id = f"receipt_{str(pet.uuid)[:32]}"

        data = {"amount": int(payment.amount * 100),"currency": "INR", "receipt": receipt_id}

        rzp_order = client.order.create(data=data)

        order_id = rzp_order['id']

        Transactions.objects.create(payment=payment,rzp_order_id=order_id,amount=payment.amount)

        return render(request, 'payments/razorpay-page.html', {
            'order_id': order_id,
            'amount': data['amount'],
            'RZP_CLIENT_ID': config('RZP_CLIENT_ID'),
            'uuid': uuid
        })

@method_decorator(csrf_exempt, name='dispatch')
class PaymentVerify(View):

    def post(self, request, *args,**kwargs):

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

            return redirect('payment-details', uuid=payment.pet.uuid)

        except razorpay.errors.SignatureVerificationError:

            transaction.status = 'Failed'

            transaction.transaction_at = datetime.datetime.now()

            transaction.save()

            return redirect('payment-details', uuid=transaction.payment.pet.uuid)

class PaymentDetailView(View):

    def get(self, request, uuid, *args, **kwargs):

        if request.user.is_superuser:  # Check if the user is an admin

            # Admin can view payment details for any pet entry
            pet = get_object_or_404(Pets, uuid=uuid)

            payment = get_object_or_404(Payment, pet=pet)
            
        else:

            customer = Customer.objects.get(profile=request.user)

            pet = get_object_or_404(Pets, uuid=uuid, customer=customer)

            payment = get_object_or_404(Payment, pet=pet)
           
           
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

            customer = Customer.objects.get(profile=request.user)

            payments = Payment.objects.filter(customer=customer)  # Regular user can only see their payments

        return render(request, 'payments/payment_list.html', {'payments': payments})

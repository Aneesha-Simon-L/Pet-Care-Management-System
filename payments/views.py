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

# @method_decorator(login_required, name='dispatch')
# class PaymentDetail(View):
#     def get(self, request, uuid, *args, **kwargs):
#         payment = get_object_or_404(Payment, pet__uuid=uuid)


#         transaction = Transactions.objects.filter(payment=payment).last()
#         context = {
#             'payment': payment,
#             'transaction': transaction
#         }
#         return render(request, 'payments/payment-details.html', context)


# Create your views here.

# class PetPaymentView(View):

#     def get(self, request, *args, **kwargs):
#         try:
#             # Get the customer's payment related to the logged-in user
#             payment = Payment.objects.get(customer__profile=request.user)
#         except Payment.DoesNotExist:
#             return render(request, 'errorpages/error-404.html')

#         # Filter transactions based on the payment and success status
#         transaction_obj = Transactions.objects.filter(payment=payment, status='Success')
#         order_id = None

#         # Check if the transaction exists and get the order_id
#         if transaction_obj.exists():
#             transaction_obj = transaction_obj.first()
#             order_id = transaction_obj.rzp_order_id
        
#         # Pass the payment and order_id to the template
#         data = {'payment': payment, 'order_id': order_id}
#         return render(request, 'payments/pet-payment-details.html', context=data)
    
# class RazorPayView(View):
#     def get(self, request, uuid, *args, **kwargs):
            
#         pet = get_object_or_404(Pets, uuid =uuid, customer=user)

#         # pet_id = kwargs.get('pet_id')

#         # with transaction.atomic():
#         #     # Make sure the pet exists and belongs to the logged-in user
#         #     pet = get_object_or_404(Pets, id=pet_id, customer__profile=request.user)

#             try:
#                 payment_obj = Payment.objects.get(customer=pet.customer)
#             except Payment.DoesNotExist:
#                 return render(request, 'errorpages/error-404.html')

#             amount = payment_obj.amount

#             # Create Razorpay order
#             client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))
#             data = {
#                 "amount": int(amount * 100),  # amount in paise
#                 "currency": "INR",
#                 "receipt": f"receipt_pet_{pet_id}"
#             }
#             payment = client.order.create(data=data)

#             order_id = payment.get('id')
#             amount = payment.get('amount')  # in paise

#             # Save transaction record
#             Transactions.objects.create(
#                 payment=payment_obj,
#                 rzp_order_id=order_id,
#                 amount=amount
#             )

#             context = {
#                 'order_id': order_id,
#                 'amount': amount,
#                 'RZP_CLIENT_ID': config('RZP_CLIENT_ID')
#             }

#             return render(request, 'payments/razorpay-page.html', context=context)


        
# @method_decorator(csrf_exempt,name='dispatch')
# class PaymentVerifyView(View):

#     def post(self,request,*args,**kwargs):

#         data = request.POST

#         rzp_order_id = data.get('razorpay_order_id')

#         rzp_payment_id = data.get('razorpay_payment_id')

#         rzp_signature = data.get('razorpay_signature')

#         transaction_obj = Transactions.objects.get(rzp_order_id = rzp_order_id)
        
#         transaction_obj.rzp_payment_id = rzp_payment_id

#         transaction_obj.rzp_signature = rzp_signature
        
#         client = razorpay.Client(auth=(config('RZP_CLIENT_ID'),config('RZP_CLIENT_SECRET')))

#         try:

#             client.utility.verify_payment_signature({
#                                                     'razorpay_order_id': rzp_order_id,
#                                                     'razorpay_payment_id': rzp_payment_id,
#                                                     'razorpay_signature': rzp_signature
#                                                     })

#             transaction_obj.status = 'Success'

#             transaction_obj.transaction_at = datetime.datetime.now()
            
#             transaction_obj.payment.status = 'Success'

#             transaction_obj.payment.paid_at = datetime.datetime.now()

#             transaction_obj.payment.save()

#             transaction_obj.save()

        
#         except:

#             transaction_obj.status = 'Failed'

#             transaction_obj.transaction_at = datetime.datetime.now() 

#             transaction_obj.save()

#         return redirect('pet-payment-details')
        




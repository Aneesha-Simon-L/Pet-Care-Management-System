from customer.models import Customer

def show_customer_name(request):
    # Set default customer name as 'Guest'
    customer_name = 'Guest'  
    
    if request.user.is_authenticated:  # Check if the user is authenticated
        
        try:
            # Try to get the 'Users' object linked to the logged-in user
            customer = Customer.objects.get(profile=request.user)

            customer_name = customer.name  # Get the customer's name

            print(customer_name)

        except Customer.DoesNotExist:
            # Handle the case where no 'Users' object is found
            customer_name = 'Guest'  # Keep the default name if user is not found

    # Always return the dictionary with the key 'customer_name'
    return {'customer_name': customer_name}

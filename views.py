from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from EcommerceHome.models import Category, Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def home(request):
    return render(request, "home.html")


def Menu(request):
    return render(request, "menu.html")

def Hover(request):
    categories = Category.objects.all()  
    return render(request, 'base.html', {'categories': categories})

def category(request, url):
    category = Category.objects.get(category_url = url)
    products = Product.objects.filter(product_category = category)
    print(category)
    print(products)
    return render(request, "category.html", {'category': category, 'products':products})

def product_detail(request, url):
    product = Product.objects.get(product_url = url)
    return render(request, "product_detail.html", {"product":product})


#login_required decorator: Ensures that only authenticated users can add items to the cart.
#If the user isn’t logged in, they will be redirected to the login page.

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(product_id = product_id)
    price = product.product_price
    #Yo chai current user ley cart create gareyko cha ki chhainna tyo tha pauna ko lagi
    #Here created holds the boolean value if cart is already created it hold true value
    #get_or_create is a function which will retrieve data if it already exits other wise create it
    cart, created = Cart.objects.get_or_create(user = request.user)
    
    #it check if the cart already has certain product or not (mathi ko user ko lagi yo product ko lagi)
    cart_item, item_created = CartItem.objects.get_or_create(cart = cart, product = product)

    #Get the quantity from the request, defaulting to 1
    quantity = int(request.GET.get('quantity', 1))

    if not item_created:
        # If the cart item already exists, increment the quantity by the passed amount
        cart_item.quantity += quantity
    else:
        # If it's a new cart item, set the quantity to the passed value
        cart_item.quantity = quantity

    cart_item.save()

    #here cart just before cartitem_set is a foreign key associated with Cartitems
    #Django will create a related manager named cartitem_set on the Cart model to 
    #give access to all the CartItem objects that are associated with a particular Cart
    total_quantity = sum(item.quantity for item in cart.cartitem_set.all())
    #total_price = sum(item.quantity * item.price for item in cart.cartitem_set.all())

    context = {
        'total_quantity': total_quantity,
      #  'total_price': total_price,
        'cart_items': cart.cartitem_set.all()
    }


    
    return render(request, "checkout.html", context)

#def sendMail():
    # subject = "This is a test mail"
    # message = "This is a test mail for checking purpose"
    # receipent_mail = ['debonairtra@hotmail.com']
    # email_from = settings.EMAIL_HOST_USER
    # send_mail(subject, message, email_from, receipent_mail)

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    total_quantity = sum(item.quantity for item in cart.cartitem_set.all())

    context = {
        'total_quantity': total_quantity,
        'cart_items': cart.cartitem_set.all(),
    }
    return render(request, "checkout.html", context)
def sendMail(request): 
    subject = "Order Confirmation"
    message = "Thank you for your order. Your order has been successfully placed!"

    recipient_mail = [request.user.email]  # Send mail to logged-in user
    recipient_mail = ["aminkhadka37@gmail.com"]
    email_from = settings.EMAIL_HOST_USER

    send_mail(subject, message, email_from, recipient_mail)

    return HttpResponse("Your order has been submitted. Check your email for confirmation.")

def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        item.quantity = new_quantity
        item.save()
    return redirect('checkout')

def delete_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        item.delete()
    return redirect('checkout')





    

    
    













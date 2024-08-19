import datetime

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import userForm
from django.views import View
from django.views import generic
from service.models import service
from OrderItem.models import OrderItem
from news.models import News
from Contact.models import Contact
from Product.models import Product
from Order.models import Order
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY



def features(request):
    # __icontains We can find the data through this function by entering only 1 word
    serviceData = service.objects.all()
    if request.method == "GET":
        st = request.GET.get('serviceData')
        if st != None:
            serviceData = service.objects.filter(service_title__icontains=st)
            print(serviceData)
    # return render(request,"features.html",{"output":output1})
    return render(request, "features.html", {"serviceData": serviceData})





def news(request):
    newsData = News.objects.all()
    data = {'newsData': newsData}
    return render(request, "news.html", data)


def newsDetails(request, newsid):
    # print(newsid)
    newsDetails = News.objects.get(
        id=newsid)  # The "get" function instead of all get only 1 row so we use it to get the data related to that entity only.
    data = {"newsDetails": newsDetails}
    return render(request, "newsDetails.html", data)


def aboutus(request):
    return render(request, "aboutus.html")


def home(request):
    newsData1 = News.objects.all()
    data = {'newsData': newsData1}
    return render(request, "home.html", data)


def products(request, slug):
    productData = Product.objects.all()
    product = Product.objects.get(product_slug=slug)
    data={'product': product,'productData':productData}
    return render(request, 'products.html', data)


def shop(request):
    product = Product.objects.all()
    productData = Product.objects.all()
    paginator = Paginator(productData, 6)
    page_number = request.GET.get('page')
    productData_final = paginator.get_page(page_number)
    total_pages = productData_final.paginator.num_pages
    data = {'productData': productData_final, 'last_page': total_pages,
            'numpage_list': [n + 1 for n in range(total_pages)], 'product': product}
    return render(request, "menu.html", data)


def ourservices(request):
    # print(newsid)
    # OurDetails=News.objects.get(id=serid)# The "get" function instead of all get only 1 row so we use it to get the data related to that entity only.
    # data={"OurDetails":OurDetails}
    serviceData = service.objects.all()
    paginator = Paginator(serviceData, 6)
    page_number = request.GET.get('page')
    serviceData_final = paginator.get_page(page_number)
    total_pages = serviceData_final.paginator.num_pages
    data = {'serviceData': serviceData_final, 'last_page': total_pages,
            'numpage_list': [n + 1 for n in range(total_pages)]}
    return render(request, "ourservices.html", data)


def contact(request):
    success = ""  # In this funtion all the logic related to form submition is written.
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        message = request.POST.get('message')
        details = Contact(name=name, email=email, phone=phone, date=date, message=message)
        details.save()
        success = "Form Submitted Succesfully"
    return render(request, "contact.html", {"success": success})


def auth(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 == pass2:

            customer = User.objects.create_user(username, email, pass1)
            customer.first_name = first_name
            customer.last_name = last_name
            customer.save()
            return redirect('userlogin')
        else:
            alert = "Both Passwords should be same!"
            return render(request, 'auth.html', {'alert': alert})

    return render(request, 'auth.html')


def userlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('userlogin')
    return render(request, 'login.html')


def userlogout(request):
    logout(request)
    return redirect('home')


# Cart:
@login_required(login_url="/userlogin/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("shop")


@login_required(login_url="/userlogin/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/userlogin/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/userlogin/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/userlogin/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/userlogin/")
def cart_detail(request):
    alert = "Your cart is empty, please add some items to your cart before checking out!"
    return render(request, 'cart/cart_detail.html', {'alert': alert})


def checkout(request):
    payment_intent = stripe.PaymentIntent.create(
        amount=50000,  # Amount in the smallest currency unit (e.g., paise for INR)
        currency="pkr",
        payment_method_types=["card"],
        capture_method="automatic"  # Automatically capture the payment
    )
    order_id = payment_intent['id']
    context = {'order_id': order_id, 'payment': payment_intent}
    return render(request, "cart/checkout.html", context)


from django.views.decorators.csrf import csrf_exempt


def placeorder(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address1') + " " + request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        order_id = request.POST.get('order_id')
        cart = request.session.get('cart')
        payment = request.POST.get('payment')
        amount = request.POST.get('amount')
        # print(name,email,address,city,state,zip_code,phone,order_id,payment)
        order = Order(
            user=user,
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            amount=amount,
            payment_id=order_id
        )
        order.save()
        for i in cart:
            a = int(cart[i]['price'])
            b = int(cart[i]['quantity'])
            total = (a * b) + 200
            item = OrderItem(
                user=user,
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=total
            )
            item.save()

        host = request.get_host()
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'pkr',
                    'product_data': {
                        'name': 'Order {}'.format(name),
                    },
                    'unit_amount': int(amount) * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="http://{}{}".format(host, reverse('payment-success')),
            cancel_url="http://{}{}".format(host, reverse('payment-cancel')),
            metadata={
                'order_id': order_id,
            }
        )

        return redirect(session.url, code=303)

    return render(request, 'confirmation.html')
def paymentsuccess(request):
    context = {
        'payment_status': "success"
    }
    return render(request, 'confirmation.html', context)


def paymentcancel(request):
    context = {
        'payment_status': "cancel"
    }
    return render(request, 'confirmation.html', context)




@csrf_exempt
def stripe_webhook(request):
    if request.method == "POST":
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            print("Payment Completed")
            session = event['data']['object']
            # Access the order_id from the metadata
            order_id = session.get('metadata', {}).get('order_id')
            print(order_id)
            if order_id:
                try:
                    order = Order.objects.get(payment_id=order_id)
                    print(f'''{order} + "hello"''')
                    order.paid = True
                    order.save()
                except Order.DoesNotExist:
                    return HttpResponse(status=404)

        return HttpResponse(status=200)

    return HttpResponse(status=400)

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import (
    CartItem,
    Cart
)
from .forms import OrderForm
import datetime
from .models import Order, Payment, OrderProduct
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from carts.views import(
    _cart_id
)


def payments(request):

    last_order = request.session.get('last_order')
    
    if request.user.is_authenticated:
        body = json.loads(request.body)
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
        print(order)

        # Store transaction details inside Payment model
        payment = Payment(
            user=request.user,
            payment_id = "hghhgj&",
            payment_method = "paypal",
            #payment_id=body['transID'],
            #payment_method=body['payment_method'],
            amount_paid=order.order_total,
            #status=body['status'],
            status = "new",
            is_guest_user = True
        )
    
    else:

        
        order = Order.objects.get(id=last_order.get('last_order_id', None))

        payment = Payment(
            payment_id = "hghhgj&",
            payment_method = "paypal",
            #payment_id=body['transID'],
            #payment_method=body['payment_method'],
            amount_paid=order.order_total,
            #status=body['status'],
            status = "new" 
        )
    
    
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # move the cart items to Order Product table

    if request.user.is_authenticated: 
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment

        if request.user.is_authenticated:
            orderproduct.user_id = request.user.id
        else:
            orderproduct.user_id = None
            orderproduct.is_guest_user = True
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.get_sale()
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()

    # clear cart
    if request.user.is_authenticated:
        CartItem.objects.filter(user=request.user).delete()
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart).delete()
    # Send order recieved email to customer
    # import html message.html file
    # mail_subject = 'Thank you for your order!'
    # to_email = request.user.email
    # html_template = 'orders/order_recieved_email.html'
    # context = {'user': request.user,'order': order,'orderproduct':orderproduct,  }
    # html_message = render_to_string(html_template, { 'context': context, })
    # send_email = EmailMessage(mail_subject, html_message, to=[to_email])
    # send_email.content_subtype = "html" 
    # send_email.send()



    mail_subject = 'Thank you for your order!'
    context = {'user': request.user,'order': order,'orderproduct':orderproduct,  }
    message = render_to_string('orders/order_recieved_email.html',context=context )

    if request.user.is_authenticated:
        to_email = request.user.email

    else:
        to_email = last_order.get('guest_mail', None)
    print("NewGuestMail=========================================================================",to_email)
    
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)

    return render(request, 'orders/payments.html', )


def place_order(request, total=0, quantity=0):

    # body = json.loads(request.body)
    # order_number=body['orderID']

    # print("order number=================================================", order_number)

    if request.user.is_authenticated:
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user) 

    else:
        oke_current_user = f"guest_user_{_cart_id(request)}"
        print("oke_user============================================================", oke_current_user)
        current_user = None
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        


    # id the cart count is less or equal then reidrect to store list of items
    #cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store:product_list')

    grand_total = 0
    tax = 0
    shipping = 0
    for cart_item in cart_items:
        total += (cart_item.product.get_sale() * cart_item.quantity)
        quantity += cart_item.quantity
    # tax =0 (2 * total)/100

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            if not request.user.is_authenticated:
                data.is_guest_user = True 
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']

            

            

            data.address = form.cleaned_data['address']
            data.municipality = form.cleaned_data['municipality']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.post_code = form.cleaned_data['post_code']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.delivery = form.cleaned_data['delivery']
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')

            if data.delivery == 'Collect From Store':
                shipping = 0
                data.shipping = shipping

            else:
                if data.country == 'greece' or data.country == 'Greece' or data.country == 'GREECE' or data.country == 'Ελλάδα' or data.country == 'ελλάδα':
                    shipping = 0
                    data.shipping = shipping

                else:
                    shipping = 13
                    data.shipping = shipping

            grand_total = total + tax + shipping

            data.order_total = grand_total


            data.save()
            last_order = Order.objects.last()
            print("last order number============================================================>", last_order.pk)
            request.session['last_order'] = {'last_order_id':last_order.pk,'guest_mail':form.cleaned_data['email']}
            #request.session['guest_mail'] = form.cleaned_data['email']
            print("Order mail========================================================>", form.cleaned_data['email'])


            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,  # optional
                'shipping': shipping,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)

    else:
        return redirect('carts:checkout')


def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        subtotal = 0
        unique_sub = 0
        for i in ordered_products:
            subtotal += i.product_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('store:product_list')

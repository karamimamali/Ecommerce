from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cartData, guestCart, guestOrder

def store(request):
    CartItems = cartData(request)['CartItems']
    products = Product.objects.all()

    context = {'products':products, 'CartItems':CartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    context = cartData(request)
    return render(request, 'store/cart.html', context)

def chechout(request):
    context = cartData(request)
    return render(request, 'store/checkout.html', context)

def detail(request, id):
    product = Product.objects.get(id=id)
    context = cartData(request)
    context['product'] = product
    return render(request, 'store/detail.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    
    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, _ = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, _ = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()

    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer 
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)

        if order.shipping:
            ShippingAdresss.objects.create(
                customer=customer,
                order= order,
                adress= data['shipping']['address'],
                city= data['shipping']['city'],
                state= data['shipping']['state'],
                zipcode= data['shipping']['zipcode']
            )

    else:
        customer, order = guestOrder(request, data)
                

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAdresss.objects.create(
            customer=customer,
            order= order,
            adress= data['shipping']['address'],
            city= data['shipping']['city'],
            state= data['shipping']['state'],
            zipcode= data['shipping']['zipcode']
        )

    return JsonResponse('Order submitted',safe=False)



import json
from .models import *

def guestCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    CartItems = order['get_cart_items']
    for key in cart:
        try:
            product = Product.objects.get(id=key)
            quantity = cart[key]['quantity']
            total = product.price * quantity
            
            

            order['get_cart_items'] += quantity
            order['get_cart_total'] += total
            CartItems += quantity

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':quantity,
                'get_total':total,
            }
            items.append(item)

            if not product.is_digital:
                order['shipping'] = True
        except:
            pass
        
    return {'items': items,  'order': order, 'CartItems':CartItems}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        CartItems = order.get_cart_items
        data = {'items': items,  'order': order, 'CartItems':CartItems}
    else:
        data = guestCart(request)

    return data


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']
    items = guestCart(request)['items']

    customer, _ = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        OrderItem.objects.create(
            product= product,
            order= order,
            quantity = item['quantity']
            )

    return customer , order
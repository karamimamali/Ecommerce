from django.db import models
from django.contrib.auth.models import User
from django_cleanup import cleanup


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(max_length=256, null=True)

    def __str__(self) -> str:
        return self.name


@cleanup.select
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    about = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.is_digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        items = sum([item.quantity for item in orderitems])
        return items


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total


class ShippingAdresss(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    adress = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.adress

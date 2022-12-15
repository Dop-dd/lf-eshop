"""
You use the product ID as a key in the cart’s content dictionary. You convert the product ID into a
string because Django uses JSON to serialize session data, and JSON only allows string key names.
The product ID is the key, and the value that you persist is a dictionary with quantity and price
figures for the product. The product’s price is converted from decimal into a string to serialize it.
Finally, you call the save() method to save the cart in the session.
"""

from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        # Initialize and store the current the cart.
        self.session = request.session
        # try to get the cart from the current session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # create and save an empty cart by setting an empty dictionary in the session.
             cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    """  create a method to add products to the cart or update their quantit"""

    def add(self, product, quantity=1, override_quantity=False):
        # Add a product to the cart or update its quantity.
       product_id = str(product.id)
       if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
       if override_quantity:
            self.cart[product_id]['quantity'] = quantity
       else:
            self.cart[product_id]['quantity'] += quantity
            self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True


    def remove(self, product):
        # Remove a product from the cart.
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            # calls the save() method to update the cart in the session
            self.save()

    """
    You will have to iterate through the items contained in the cart and access the related Product
    instances. To do so, we can define an __iter__() method in your class. Ltes add the following
    method to the Cart class:
    """
    def __iter__(self):
        # Iterate over the items in the cart and get the products from the database.
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    """
    Next, define a custom __len__() method to return the total number of items
    stored in the cart.
    """
    def __len__(self):
        # Count all items in the cart.
        return sum(item['quantity'] for item in self.cart.values())


    """ Add the following method to calculate the total cost of the items in the cart: """
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    """ Finally, add a method to clear the cart session: """
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()


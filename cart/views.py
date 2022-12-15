"""
1. Use the require_POST decorator to allow only POST requests. The view receives the product ID
    as a parameter.
2. You retrieve the Product instance with the given ID and validate CartAddProductForm.
3. If the form is valid, you either add or update the product in the cart.
4. The view redirects to the cart_detail URL, which will display the contents of the cart
"""


from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


# Add product to cart
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])
    return redirect('cart:cart_detail')


"""
The cart_remove view receives the product ID as a parameter. You use the require_POST decorator to
allow only POST requests. You retrieve the Product instance with the given ID and remove
 the product from the cart. Then, you redirect the user to the cart_detail UR
"""
# # Remove product to cart
@require_POST
def cart_remove(request, product_id):
    cart =Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


# view to display the cart and its item
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

"""
Done, next Create a new file inside the cart application directory and name it urls.py
to add URL patterns for these views
"""
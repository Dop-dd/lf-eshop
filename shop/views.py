from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm


# Building catalog views
# Product list  views
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    # retrieve only available products.
    products = Product.objects.filter(available=True)
    # optionally filter products by a given category
    if category_slug:
        category = get_object_or_404(Category,
                                    slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html',
                    {'category': category,
                    'categories': categories,
                    'products': products})

# Product detail views
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id,
                                slug=slug, available=True)

    cart_product_form = CartAddProductForm()
    # retieves the product instance based on id and slug params
    return render(request,
                    'shop/product/detail.html',
                    {'product': product,
                    'cart_product_form': cart_product_form})
from django import forms

# allows the user to select a quantity between 1 and 20
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    """  use a TypedChoiceField field with coerce=int to convert the input into an integer """
    quantity = forms.TypedChoiceField(
                                    choices=PRODUCT_QUANTITY_CHOICES,
                                    coerce=int)

    """
    indicate whether the quantity has to be added to any existing quantity in the cart for this
    product (False), or whether the existing quantity has to be overridden with the given quantity (True)
    use a HiddenInput to hide widget from display
    """
    override = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)



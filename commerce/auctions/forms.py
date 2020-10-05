from typing import Any
from django import forms


class CreateListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=2048)
    starting_bid = forms.DecimalField(max_digits=8)
    image_url = forms.CharField(max_length=2048, required=False)
    category = forms.CharField(max_length=64, required=False)
    #closed = forms.BooleanField(initial=False)

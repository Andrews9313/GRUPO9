from django import forms
from django.forms import formset_factory
from .models import Invoice, LineItem
from django.forms import ModelForm, inlineformset_factory


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'customer_email', 'billing_address', 'date', 'due_date', 'message', 'total_amount', 'status']

#
# class InvoiceForm(forms.Form):
#     # fields = ['customer', 'message']
#     customer = forms.CharField(
#         label='Cusomter',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Customer/Company Name',
#             'rows': 1
#         })
#     )
#     customer_email = forms.CharField(
#         label='Customer Email',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'customer@company.com',
#             'rows': 1
#         })
#     )
#     billing_address = forms.CharField(
#         label='Billing Address',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': '',
#             'rows': 1
#         })
#     )
#     message = forms.CharField(
#         label='Message/Note',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'message',
#             'rows': 1
#         })
#     )
#
#     metodoenvio = forms.CharField(
#         label='Metodo/envio',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'metodoenvio',
#             'rows': 1
#         })
#     )
#
#     metodopago = forms.CharField(
#         label='metodo/pago',
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'metodopago',
#             'rows': 1
#         })
#     )


class LineItemForm(forms.ModelForm):
    class Meta:
        model = LineItem
        fields = ['service', 'description']
    # service = forms.CharField(
    #     label='Service/Product',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control input',
    #         'placeholder': 'Service Name'
    #     })
    # )
    # description = forms.CharField(
    #     label='Description',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control input',
    #         'placeholder': 'Enter Book Name here',
    #         "rows": 1
    #     })
    # )
    quantity = forms.IntegerField(
        label='Qty',
        widget=forms.TextInput(attrs={
            'class': 'form-control input quantity',
            'placeholder': 'Quantity'
        })  # quantity should not be less than one
    )
    rate = forms.DecimalField(
        label='Rate $',
        widget=forms.TextInput(attrs={
            'class': 'form-control input rate',
            'placeholder': 'Rate'
        })
    )
    # amount = forms.DecimalField(
    #     disabled = True,
    #     label='Amount $',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control input',
    #     })
    # )


LineItemFormset = inlineformset_factory(Invoice, LineItem, form=LineItemForm, extra=1)
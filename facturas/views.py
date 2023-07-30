from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View


from ventas.models import Cliente
from .models import LineItem, Invoice
from .forms import LineItemFormset, InvoiceForm, LineItemForm

import pdfkit


class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices": invoices,
        }

        return render(self.request, 'invoice/invoice-list.html', context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('invoice:invoice-list')


def createInvoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices,
    this will be protected view, only admin has the authority to read and make
    changes here.
    """
    global invoice, formset, form
    heading_message = 'Formset Demo'
    LineItemFormset = modelformset_factory(LineItem, form=LineItemForm, extra=1)
    if request.method == 'GET':
        formset = LineItemFormset(queryset=LineItem.objects.none())
        form = InvoiceForm()
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)

        if form.is_valid():
            cliente = Cliente.objects.get(pk=1)  # Obtener cliente con id 1
            invoice = form.save(commit=False)
            invoice.customer = cliente
            invoice.total_amount = 0
            invoice.save()

            if form.cleaned_data.get('customer'):
                invoice.customer = form.cleaned_data['customer']
                invoice.save()

        if formset.is_valid():
            total = 0
            for form in formset:
                if form.cleaned_data.get('service') and form.cleaned_data.get('description') and form.cleaned_data.get('quantity') and form.cleaned_data.get('rate'):
                    lineitem = form.save(commit=False)
                    lineitem.customer = invoice
                    lineitem.amount = form.cleaned_data['rate'] * form.cleaned_data['quantity']
                    total += lineitem.amount
                    lineitem.save()

            invoice.total_amount = total
            invoice.save()

            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/')
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'invoice/invoice-create.html', context)


def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()

    context = {
        "company": {
            "name": "CINEMARK",
            "address": "AV QUITO Y GOMEZ RENDON",
            "phone": "0968974251",
            "email": "CinesM@gmail.com",
        },
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice.date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "lineitem": lineitem,

    }
    return render(request, 'invoice/pdf_template.html', context)


def generate_PDF(request, id):
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe')
    # configurations: Configuration = pdfkit.configuration(wkhtmltopdf='C:/Program Files (x86)/wkhtmltopdf/bin/wkhtmltopdf.exe')

    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail', args=[id])), False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response


def change_status(request):
    return redirect('invoice:invoice-list')


def view_404(request, *args, **kwargs):
    return redirect('invoice:invoice-list')
import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse

from orders.models import Order, OrderItem
from django.utils.safestring import mark_safe


def order_detail(obj):
    """Custom order admin field"""
    URL = reverse("orders:admin_order_detail", args=[obj.id])
    return mark_safe(f"<a href='{URL}'>View</a>")


order_detail.short_description = 'Detail'


def export_to_pdf(obj):
    """Custom field to download pdf"""
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f"<a href='{url}'>PDF</a>")


export_to_pdf.short_description = 'Download'


def export_to_csv(modeladmin, request, queryset):
    """Custom admin action to download orders as CSV file"""
    opts = modeladmin.model._meta
    content_disposition = 'attachment; filename={opts.verbose_name}.csv'

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not \
        field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


class OrderItemAdmin(admin.TabularInline):
    """Order Item Inline admin panel"""
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order Admin panel"""
    list_display = ('first_name', 'last_name', 'address', 'postal_code',
                    'city', 'created', 'updated', 'paid', order_detail, export_to_pdf)
    list_filter = ('paid', 'created', 'updated')
    inlines = (OrderItemAdmin,)
    actions = (export_to_csv,)

import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import OrderItem, Order

# Register your models here.
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment;filename={opts.verbose_name}.csv"
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if field.many_to_many or field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    
    data_row = []
    for obj in queryset:
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d")
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = "Export to CSV"


def order_detail(obj):
    return mark_safe(f"<a href=\"{reverse('orders:admin_order_detail', args=[obj.id])}\">Detail</a>")

order_detail.short_description = "Detail"


def order_pdf(obj):
    return mark_safe(f"<a href=\"{reverse('orders:admin_order_pdf', args=[obj.id])}\">PDF</a>")
order_pdf.short_description = "PDF"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]
    
class OrderAdmin(admin.ModelAdmin):
    # list_display = ["id", "first_name", "last_name", "email", "address", "postal_code", "city", "paid", order_detail, order_pdf, "created", "updated"]
    list_display = ["id", "first_name", "last_name", "email", "address", "postal_code", "city", "paid", "created", "updated"]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]
    actions = [export_to_csv]

admin.site.register(Order, OrderAdmin)    
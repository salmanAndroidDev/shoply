from io import BytesIO
import weasyprint
from celery import task
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

from orders.models import Order


@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created
    """
    order = Order.objects.get(id=order_id)
    subject = f"Order nr.{order_id}"
    message = f"Dear {order.first_name},\n\n" \
              f"You have successfully placed an order." \
              f"Your order ID is {order.id}"
    mail_sent = send_mail(subject,
                          message,
                          'admin@shoply.com',
                          [order.email])
    return mail_sent


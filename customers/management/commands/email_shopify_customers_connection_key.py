from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.urls import reverse

from customers.models import Connection, ConnectionKey


class Command(BaseCommand):
    help = "Email customers with a link that can be used to authorize a Shopify OAuth application"

    def handle(self, *args, **options):
        for connection in Connection.objects.filter(connection_type="Shopify").select_related("customer"):
            connection_key = get_random_string(length=32)
            key = ConnectionKey(
                **{
                    'connection': connection,
                    'connection_key': connection_key
                }
            )
            key.save()

            send_mail(
                "Please authorize your Shopify Account",
                f"We are moving from API Keys to OAuth for Shopify. Please use this link {settings.HOSTNAME}{reverse('generate_oauth_link_from_key', args=[connection_key])}",
                "from@example.com",
                [connection.customer.email],
                fail_silently=False,
            )

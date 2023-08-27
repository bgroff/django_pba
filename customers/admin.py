from django.contrib import admin

from customers.models import Customer, Connection, ConnectionKey


# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    pass


@admin.register(ConnectionKey)
class ConnectionAdmin(admin.ModelAdmin):
    pass

from django.db import models


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=255)
    workspace_id = models.CharField(max_length=255)
    email = models.EmailField()


class Connection(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    connection_id = models.CharField(max_length=255)
    source_id = models.CharField(max_length=255)
    destination_id = models.CharField(max_length=255)
    connection_type = models.CharField(max_length=255)


class ConnectionKey(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.DO_NOTHING)
    connection_key = models.CharField(max_length=255, primary_key=True)

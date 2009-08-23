from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CheapProductManager(models.Manager):
    def get_query_set(self):
        return super(CheapProductManager, self).get_query_set().filter(price__lte=100)

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    
    objects = models.Manager() # Koniecznie potrzebny
    cheap_products = CheapProductManager()
    @staticmethod
    def get_ordered_by_price():
        return Product.objects.all().order_by('price')

class Client(models.Model):
    fullname = models.CharField(max_length=120)
    products = models.ManyToManyField(Product)
    user = models.OneToOneField(User)

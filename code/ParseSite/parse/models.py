from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=1000, verbose_name="")
    status = models.IntegerField(default=0)
    
    def __str__(self):
        return self.doc_name

class Product(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    citilink_id = models.IntegerField()
    product_name = models.CharField(max_length=1000)
    search_name = models.CharField(max_length=1000,blank=True,null=True)
    is_done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.product_name
    
class WBProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url = models.CharField(max_length=1000)
    
class Store(models.Model):
    document = models.ManyToManyField(Document)
    name = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.name

class DataResourse(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE,blank=True,null=True)
    data = JSONField()
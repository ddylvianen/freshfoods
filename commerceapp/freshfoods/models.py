from django.db import models
from django.contrib.auth.models import User
from compressed_image_field import CompressedImageField

class payment_info(models.Model):
   card_number = models.IntegerField(null=True)
   exp_number = models.DateField(null=True)
   cvc_number = models.IntegerField(null=True)
   cardholder = models.CharField(max_length=200, null=True)

class adress(models.Model):
   streetname = models.CharField(max_length=100, null=True)
   streetnumber = models.IntegerField(null=True)
   postcode = models.CharField(max_length=6, null=True)

   def __str__(self):
     return self.streetname

class profileUser(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   img = CompressedImageField(null=True, upload_to='profiles', default='default_profile.jpg', quality=10)
   birthday = models.DateField(null=True, blank=True)
   adress = models.ForeignKey(adress, null=True, blank=True, on_delete=models.SET_NULL)
   payment_info = models.OneToOneField(payment_info, null=True, blank=True, on_delete=models.SET_NULL)

   def __str__(self):
      return self.user.username

   
class tag(models.Model):
    tags = models.CharField(max_length=50, null=True)

    def __str__(self):
       return self.tags

class product(models.Model):
    name = models.CharField(max_length=50, null=True)
    discription = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=18, null=True)
    discount = models.IntegerField(null=True, default=0)
    tags = models.ForeignKey(tag, null=True, on_delete=models.SET_NULL)
    img = CompressedImageField(upload_to='products', default="default_product.jpg", null=True, quality=50)
    lastupdate = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def discount_price(self):
      return round(float(self.price) - ((self.discount / 100) * float(self.price)),2)
    
    def __str__(self):
      return self.name
    

class cart_item(models.Model):
   invoice = models.CharField(max_length=50, null=True, default="")
   user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   item = models.ForeignKey(product, null=True, on_delete=models.CASCADE)
   quantity = models.IntegerField(null=True, default=1)
   price = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=18)

   def remove_item(self):
       self.quantity -= 1
       self.price_item()
       if(self.quantity == 0):
         self.delete()
       else:
          self.save()

   def add_item(self):
      self.quantity += 1
      self.price_item()
      self.save()

   def price_item(self):
      self.price = round((float(self.item.discount_price()) * self.quantity), 2)
      self.save()

   def add_invouce(self, invoise):
      self.invoice = invoise
      self.price_item()
      self.save()

   def __str__(self):
      return f"{self.item.name} of {self.user.username}"


class shoppingcart(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
   products = models.ManyToManyField(cart_item, default=None)
   def total_item(self):
      total = 0
      for i in self.products.all():
         total += i.quantity
      return total

   def total_price(self):
      total = 0
      print(self.products.all())
      for i in self.products.all():
         i.price_item()
         total += i.price
      return total
   def remove_item(self, item):
      self.products.remove(item)
      self.save()
   
   def __str__(self):
      return "cart of " + self.user.username


class order(models.Model):
   STATUS = (('PENDING','PENDING'), 
             ('PACKING', 'PACKING'), 
             ('ON THE WAY', 'ON THE WAY'), 
             ('COMPLETED', 'COMPLETED'), 
             ('REJECTED', 'REJECTED'))

   user = models.ForeignKey(User, null=True,on_delete=models.SET_NULL)
   product = models.ManyToManyField(cart_item)
   status = models.CharField(max_length=50, default=1, choices=STATUS)
   invoice = models.CharField(max_length=50, null=True, blank=True, unique=True, auto_created=True)
   date = models.DateField(auto_now_add=True, null=True)

   def __str__(self):
      return self.invoice


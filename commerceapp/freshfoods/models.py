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

    def __str__(self):
      return self.name
    

class cart_item(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
   item = models.ForeignKey(product, null=True, on_delete=models.CASCADE)
   quantity = models.IntegerField(null=True, default=1)

   def __str__(self):
      return f"{self.item.name} of {self.user.username}"


class shoppingcart(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
   products = models.ManyToManyField(cart_item, default=None)
   total_items = models.IntegerField(null=True, default=0)

   
   def __str__(self):
      return "cart of " + self.user.username


class order(models.Model):
   STATUS = ((1,'PENDING'), 
             (2, 'PACKING'), 
             (3, 'ON THE WAY'), 
             (4, 'COMPLETED'), 
             (5, 'REJECTED'))

   user = models.OneToOneField(User, null=True,on_delete=models.SET_NULL)
   product = models.ForeignKey(product, null=True, on_delete=models.DO_NOTHING)
   status = models.CharField(max_length=50, default=1, choices=STATUS)
   invoice = models.CharField(max_length=50, null=True, blank=True)
   date = models.DateField(null=True, blank=True)

   def __str__(self):
      return self.invoice


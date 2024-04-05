from django.db import models
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

# Create your models here.
class CustomerReg(models.Model):
    name=models.CharField(max_length=200)
    mobile_number=models.CharField(max_length=15)
    whatsapp_number=models.CharField(max_length=15)
    email=models.EmailField(blank=True,null=True)
    date_of_birth=models.DateField()
    username=models.CharField(max_length=20,null=True,unique=True,blank=True)
    password=models.CharField(max_length=100)
    conform_password=models.CharField(max_length=100)


    # def save(self, *args, **kwargs):
    #     if not self.pk :  # Only for new instances
    #         if not self.username:
    #             self.username = self.generate_username()
                
    #         if self.password == self.conform_password:
    #             self.password = make_password(self.password)
    #             self.conform_password = make_password(self.conform_password)

    #         try:
    #              super().save(*args, **kwargs)
    #         except IntegrityError:
    #             self.username = self.generate_username()


            
       
        
    # def generate_username(self):
    #     first_chars=self.name[:4].lower()

    #     last_mobile=self.mobile_number[-4:]

    #     year_last=str(self.date_of_birth.year)[-2:]

    #     return first_chars + last_mobile + year_last
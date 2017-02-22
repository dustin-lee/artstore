from __future__ import unicode_literals
from django.db import models
from django.contrib.contenttypes import fields
# import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
ONLY_LETTERS = re.compile('\d') #checks for a digit
ONECAP_ONENUM = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$') #one capital one number

class UserManager(models.Manager):
    def login(self, post):
        user_list = AdminUser.objects.filter(email = post['email'])
        if user_list:
            user = user_list[0]
            if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password:
                return user
        return None

    def register(self, post):
        encrypted_password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
        AdminUser.objects.create(name = post['name'], username = post['username'], email = post['email'], password = encrypted_password )

    def validate(self, post):
        errors = []

        if len(post['name']) == 0:
            errors.append("Name is required")
        elif len(post['name']) < 3:
            errors.append("Name must be at least 3 characters")
        elif not post['name'].isalpha():
            errors.append("Only letters, BOO")

        if len(post['alias']) == 0:
            errors.append("Alias is required")
        elif len(post['alias']) < 3:
            errors.append("Alias must be at least 3 characters")
        elif not post['alias'].isalpha():
            errors.append("Only letters, BOO")

        if len(post['email']) == 0:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(post['email']):
            errors.append("Please enter a valid email")

        if len(post['password']) == 0:
            errors.append("Must enter a password")
        elif len(post['password']) < 8:
            errors.append("Password must have at least 8 characters")
        elif post['password'] != post['confirm_pass']:
            errors.append("Password and confirmation must match")

        if len(AdminUser.objects.filter(email = post['email'])) > 0 :
            errors.append("Email address is unavailable!")

        return errors

class AdminUser(models.Model):
    name = models.CharField(max_length = 45)
    username = models.CharField(max_length = 45)
    email = models.EmailField(max_length= 60)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Billing(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    zipcode = models.IntegerField()
    token = models.CharField(max_length=255, default=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Shipping(models.Model):
    name = models.CharField(max_length = 45, default=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=45)
    state = models.CharField(max_length=45)
    zipcode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to="products/")
    description = models.CharField(max_length=45)
    categories = models.CharField(max_length=45)
    price = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField()

class Cart_product(models.Model):
    product = models.ForeignKey(Product)
    objects = UserManager()

class Cart(models.Model):
    cart_product = models.ForeignKey(Cart_product)
    objects = UserManager()

class Gen_user(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cart = models.ForeignKey(Cart)
    objects = UserManager()

class Order(models.Model):
    cart = models.OneToOneField(Cart)
    objects = UserManager()

class Log_user(models.Model):
    username = models.CharField(max_length=45)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order)
    billing = models.ForeignKey(Billing)
    shipping = models.ForeignKey(Shipping)
    objects = UserManager()

class Gen_user_product(models.Model):
    gen_user = models.ForeignKey(Gen_user)
    product = models.ForeignKey(Product)
    objects = UserManager()

class Log_user_product(models.Model):
    log_user = models.ForeignKey(Log_user)
    product = models.ForeignKey(Product)
    objects = UserManager()

class Order_product(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    count = models.IntegerField()
    objects = UserManager()

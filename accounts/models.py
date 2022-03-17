from django.db import models
import re

from django.db.models.deletion import CASCADE

class UserManager(models.Manager):
    def basic_validator(self, postData, reqFILES):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters!"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters!"
        if len(reqFILES) == 0:
            errors['pfp'] = "Please upload an image!"
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters!"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match!"
        return errors

class FoodManager(models.Manager):
    def basic_validator(self, postData, reqFILES):
        errors = {}
        if len(postData['title']) < 8:
            errors['title'] = "Title should be at least 8 characters!"
        if len(reqFILES) == 0:
            errors['food_pic'] = "Please upload an image of the food!"

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    pfp = models.ImageField(null=True, blank=True, upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Food(models.Model):
    title = models.CharField(max_length=55)
    food_image = models.ImageField(null=True, blank=True, upload_to="images/")
    food_uploader = models.ForeignKey(User, related_name="users_food", on_delete = models.CASCADE)
    user_comments = models.ManyToManyField(User, related_name="all_food_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FoodManager()
from django.db import models
import re

class UserManager(models.Manager):
    def user_validator(self, postData):
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long"
        if not email_check.match(postData['email']):             
            errors['email'] = "Invalid email address"
        if len(postData['pw']) < 8:
            errors['pw_length'] = "Password must be at least 8 characters"
        if postData['pw'] != postData['pw_confirm']:
            errors['pw_match'] = "Password does not match Confirm Password"
        return errors
    def update_validator(self, postData):
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long"
        if not email_check.match(postData['email']):             
            errors['email'] = "Invalid email address"
        return errors
    def login_validator(self, postData):
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if not email_check.match(postData['email']):             
            errors['email'] = "Invalid email address"
        if len(postData['pw']) < 8:
            errors['pw_length'] = "Password must be at least 8 characters"        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    pw = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    # quotes = quotes posted by user
    # liked_quotes = a list of quotes a user liked

class QuoteManager(models.Manager):
    def quote_validator(self, postdata):
        errors = {}
        if len(postdata['author']) < 3:
            errors['author'] = "Author name must be more than 3 characters"
        if len(postdata['quote']) < 10:
            errors['quote'] = "Quote must be more than 10 characters"
        return errors

class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length = 255)
    user = models.ForeignKey(User, related_name = 'quotes', on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name = "liked_quotes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = QuoteManager()

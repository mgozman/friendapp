from __future__ import unicode_literals
from django.db import models
import os

import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class showManager(models.Manager):
    def basic_validator_reg(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        
        if postData['email'] != '':
            if not EMAIL_REGEX.match(postData['email']): 
                errors["email"] = "Email is not valid"     

            if self.filter(email = postData['email']):
                errors['email'] = "User with this email as already exists"

        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"

        if postData['password'] != postData['password_confirm']:
            errors["password_confirm"] = "Passwords don't match"
        return errors

    def basic_validator_login(self, postData):
        errors = {}
        if postData['login'] != '':
            if len(self.filter(email = postData['login'])) == 0:
                errors['login'] = "User with this email isn't exists"
        return errors

    def trip_validator(self, postData):
        errors = {}
        if len(postData['dest']) < 3:
            errors['destination'] = "Destination must be at least 3 characters"
        if len(postData['plan']) < 3:
            errors['plan'] = "Plan must be at least 3 characters"
        return errors

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)

class users (models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)

    profile_image = models.ImageField(upload_to = 'user_images/', default = '/user_images/no-pics.jpg')
    status = models.CharField(max_length=255, default = 'my status')
    online_status = models.BooleanField(default = False)
    city = models.CharField(max_length=45, default = 'My city')
    marrige = models.CharField(max_length=45, default = 'Single')
    phone = models.IntegerField(default = 1111111111)
    skype = models.CharField(max_length=45, default = 'my skype')
    school = models.CharField(max_length=45, default = 'my school')

    friends = models.ManyToManyField('self')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = showManager()
    def __reprexit_(self):
        return f"Users: {self.id} ({self.first_name}, {self.last_name}, {self.email}, {self.password}, {self.profile_image}, {self.created_at}, {self.updated_at}) "

class Posts (models.Model):
    post = models.TextField()
    user_who_created = models.ForeignKey(users, on_delete=models.CASCADE, related_name="all_created_posts")
    user_where_posted = models.ForeignKey(users, on_delete=models.CASCADE, related_name="all_posts_on_my_wall")
    users_who_liked = models.ManyToManyField(users, related_name = "liked_posts")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    def __repr__(self):
        return f"Posts: {self.id} ({self.post}, {self.user_who_created}, {self.users_who_liked}, {self.created_at}, {self.updated_at}) "

class Comments (models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="all_comments")
    user_who_created = models.ForeignKey(users, on_delete=models.CASCADE, related_name="created_comments")
    users_who_liked = models.ManyToManyField(users, related_name = "liked_comments")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    def __repr__(self):
        return f"Comments: {self.id} ({self.comment}, {self.user_who_created}, {self.users_who_liked}, {self.created_at}, {self.updated_at}) "

class Messages (models.Model):
    message = models.TextField()
    
    user_from = models.ForeignKey(users, on_delete=models.CASCADE, related_name="messages_from")
    user_to = models.ForeignKey(users, on_delete=models.CASCADE, related_name="messages_to")
    was_read = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    def __repr__(self):
        return f"Messages: {self.id} ({self.message}, {self.user_from}, {self.user_to}, {self.created_at}, {self.updated_at}) "

class Groups (models.Model):
    title = models.TextField()
    desc = models.TextField()
    profile_image = models.ImageField(upload_to = 'user_images/', default = '/login_app/images/no-pics.jpg')

    user_who_created = models.ForeignKey(users, on_delete=models.CASCADE, related_name="created_groups")
    users = models.ManyToManyField(users, related_name = "my_groups")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    def __repr__(self):
        return f"GROUP: {self.id} ({self.title}, {self.desc}, {self.user_who_created}, {self.created_at}, {self.updated_at}) "

class Images (models.Model):
    user = models.ForeignKey(users, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to = 'user_images/', default = '/user_images/no-pics.jpg')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    def __repr__(self):
        return f"Images: {self.id} ({self.user}, {self.created_at}, {self.updated_at}) "
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name
    

class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=600)
    minBid = models.DecimalField(max_digits=20, decimal_places=2)
    imgURL = models.CharField(max_length=16000, blank=True)
    active = models.BooleanField(default=True,blank=True,null=True)
    bids = models.IntegerField(default=0)
    seller = models.ForeignKey("User", on_delete=models.CASCADE,related_name='seller')
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    highestBidder = models.ForeignKey("User", on_delete=models.CASCADE, blank=True,related_name='buyer',null=True,db_constraint=False)
    def __str__(self):
        return self.title


class Watch(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='watcher')
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name='item')
    def __str__(self):
        return f'{self.user.username} is watching {self.listing.title}'

class Comment(models.Model):
    msg = models.TextField(max_length=400)
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name='listing')
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='commentor',null=True,db_constraint=False, blank=True)
    def __str__(self):
        return f"{self.user.username} : {self.msg} about {self.listing.title}"
    
   
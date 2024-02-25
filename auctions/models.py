from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone


class User(AbstractUser):
    def __str__(self):
        return f'{self.first_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=64, verbose_name='name')

    def __str__(self):
        return f'{self.category_name}'


class Bid(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_bid', verbose_name='bidder')
    bid = models.FloatField()
    date_posted = models.DateTimeField(default=django.utils.timezone.now, verbose_name='bid date')

    def __str__(self):
        return f'{self.author} on {self.date_posted}'


class Listing(models.Model):
    title = models.CharField(max_length=30, verbose_name='title')
    description = models.CharField(max_length=100, verbose_name='description')
    img_url = models.CharField(max_length=1000, verbose_name='img_url')
    price = models.ForeignKey(Bid, blank=True, null=True, related_name='listingbid',verbose_name=("price"), on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')
    is_active = models.BooleanField(default=True, verbose_name='status')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user', verbose_name='user')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='user_category', verbose_name='category')
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingwatchlist", verbose_name="user watchlist")


    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_comment', verbose_name='user comment')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name='listing_comment', verbose_name='listing comment')
    message = models.CharField(max_length=200)
    date_posted = models.DateTimeField(default=django.utils.timezone.now, verbose_name='date posted')
    
    def __str__(self):
        return f'{self.author} comments on {self.listing} on {self.date_posted}'



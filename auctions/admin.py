from django.contrib import admin
from .models import User, Category, Listing, Comment, Bid
# Register your models here.
# class FlightAdmin(admin.ModelAdmin):
#     

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name')


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'title', 'price', 'date_created', 'owner', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'listing', 'message', 'date_posted')


class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'bid', 'date_posted')


# class WatchlistAdmin(admin.ModelAdmin):
#     list_display = ('id', 'author', 'listing', 'date_added')

admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
# admin.site.register(Watchlist, WatchlistAdmin)
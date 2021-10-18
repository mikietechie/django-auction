from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id','name'
    ]

admin.site.register(Category,CategoryAdmin)

class WatchAdmin(admin.ModelAdmin):
    list_display = [
        'id','user','listing'
    ]

admin.site.register(Watch,WatchAdmin)

class ListingAdmin(admin.ModelAdmin):
    list_display = [
        'id','title','minBid','category','seller','highestBidder'
    ]

admin.site.register(Listing,ListingAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id','msg','listing','user'
    ]

admin.site.register(Comment,CommentAdmin)

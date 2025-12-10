from django.contrib import admin
from .models import Board, SavedImage, BoardItem, Profile
from .models import Vendor, BlogPost, Inspiration

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'category', 'created_at')
    search_fields = ('name', 'owner__username', 'category')

@admin.register(SavedImage)
class SavedImageAdmin(admin.ModelAdmin):
    list_display = ('board', 'title', 'saved_at')
    search_fields = ('title', 'board__name')

@admin.register(BoardItem)
class BoardItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'created_at')
    search_fields = ('name', 'board__name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'location', 'gender')
    search_fields = ('user__username', 'phone_number', 'location')

# Simple registrations without custom admin
admin.site.register(Vendor)
admin.site.register(BlogPost)
admin.site.register(Inspiration)

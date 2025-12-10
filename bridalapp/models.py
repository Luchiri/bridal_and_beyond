from django.db import models
from django.contrib.auth.models import User

CATEGORY_CHOICES = [
    ('Bridal', 'Bridal'),
    ('Groom', 'Groom'),
    ('Accessories', 'Accessories'),
    ('Decor', 'Decor'),
]

class Board(models.Model):
    name = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='boards/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boards')
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def items_count(self):
        return self.saved_images.count()


class SavedImage(models.Model):
    board = models.ForeignKey(Board, related_name='saved_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='board_items/')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image on {self.board}"

class BoardItem(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # URL from your website
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or "Board Item"

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    instagram = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"
    
class Vendor(models.Model):
    CATEGORY_CHOICES = [
    ("Wedding Planner", "Wedding Planner"),
    ("Photographer", "Photographer"),
    ("Makeup Artist", "Makeup Artist"),
    ("Hair Stylist", "Hair Stylist"),
    ("Cake Designer", "Cake Designer"),
    ("Florist", "Florist"),
    ("Decor Stylist", "Decor Stylist"),
    ("Dress Designer", "Dress Designer"),
    ("Suit Designer", "Suit Designer"),
    ("Caterer", "Caterer"),
    ("Venue", "Venue"),
    ("Invitation Designer", "Invitation Designer"),
]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)  # e.g. "Nairobi"
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='vendors/')
    phone = models.CharField(max_length=50, blank=True)
    whatsapp = models.URLField(blank=True)
    instagram = models.URLField(blank=True)

    def __str__(self):
        return self.name
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog-tips/')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Inspiration(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='inspirations/')
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
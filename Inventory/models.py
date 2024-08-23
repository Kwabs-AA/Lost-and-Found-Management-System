from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Lost(models.Model):
    CATEGORY_CHOICES = [
        ('ID', 'ID'),
        ('Wallet', 'Wallet'),
        ('Keys', 'Keys'),
        ('Phone', 'Phone'),
        ('Laptop', 'Laptop'),
        ('Tablet', 'Tablet'),
        ('Clothing', 'Clothing'),
        ('Jewelry', 'Jewelry'),
        ('Backpack', 'Backpack'),
        ('Headphones', 'Headphones'),
        ('Glasses', 'Glasses'),
        ('Books', 'Books'),
        ('Documents', 'Documents'),
        ('Other', 'Other'),
    ]

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='lost_images/')
    lostdesc = models.TextField(blank=True, null=True)  # Updated to be optional
    name = models.CharField(max_length=255, blank=True, null=True)  # Updated to be optional
    indexNo = models.IntegerField(blank=True, null=True)  # Updated to be optional
    location = models.TextField()
    uploader_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category}: {self.name if self.name else 'Unnamed'}"

class Review(models.Model):
    reviewer_name = models.ForeignKey(User, on_delete=models.CASCADE)
    lost_item = models.ForeignKey(Lost, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uploader_name = models.TextField()

class Badges(models.Model):
    uploader_name = models.CharField(max_length=255)
    count = models.IntegerField(default=0)

    def get_badge_type(self):
        if self.count >= 50:
            return 'Trustworthy'
        elif self.count >= 25:
            return 'Reliable'
        elif self.count >= 10:
            return 'Proven'
        return 'No Badge'

    @staticmethod
    def get_highest_count_user():
        return Badges.objects.order_by('-count').first()


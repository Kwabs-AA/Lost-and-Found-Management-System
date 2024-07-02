from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Lost(models.Model):
    CATEGORY_CHOICES = [
        ('ID', 'ID'),
        ('Personal Belongings', 'Personal Belongings'),
        ('Devices', 'Devices'),
    ]

    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='lost_images/')
    lostdesc = models.TextField()
    name = models.CharField(max_length=255) 
    indexNo = models.IntegerField()
    location = models.TextField()
    uploader_name=models.CharField(max_length=255)

class Review(models.Model):
    reviewer_name=models.ForeignKey(User,on_delete=models.CASCADE)
    lost_item=models.ForeignKey(Lost,on_delete=models.CASCADE)
    rating=models.IntegerField(choices=[(i,i)for i in range (1,6)])
    review_text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    uploader_name=models.TextField()
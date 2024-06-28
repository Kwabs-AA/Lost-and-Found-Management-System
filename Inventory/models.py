from django.db import models

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
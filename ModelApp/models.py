from django.db import models

class Review(models.Model):
    ReviewId = models.AutoField(primary_key=True)
    Source = models.CharField(max_length = 300)
    Destination = models.CharField(max_length = 300)
    Description = models.CharField(max_length = 300)
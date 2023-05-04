from django.db import models

class Administrator(models.Model):
    adminId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)   
    password = models.CharField(max_length=128)

    # Define a custom manager to retrieve the singleton instance
    objects = models.Manager()

    def save(self, *args, **kwargs):
        # Override the save method to ensure only one instance is saved
        self.pk = 1  # Set the primary key to 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        # Custom manager method to retrieve the singleton instance
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

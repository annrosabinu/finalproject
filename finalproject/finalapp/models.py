from django.db import models
from django.contrib.auth.models import User
from .models import UserProfile


class Package(models.Model):
    name = models.CharField(max_length=100)
    validity_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    height = models.CharField(max_length=10)
    job_designation = models.CharField(max_length=100)
    job_place = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    religion = models.CharField(max_length=100)
    caste = models.CharField(max_length=100)
    marriage_level = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    sibling_name = models.CharField(max_length=100)
    sibling_status = models.CharField(max_length=10)  # Married/Unmarried
    profile_pictures = models.ImageField(upload_to='profile_pics/')
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()

    def __str__(self):
        return self.user.username

class ChatRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('blocked', 'Blocked')])

    def __str__(self):
        return f"Chat Request from {self.from_user.username} to {self.to_user.username}"


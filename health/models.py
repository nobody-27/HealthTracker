from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class HealthRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record_date = models.DateField()
    symptoms = models.TextField()
    condition = models.CharField(max_length=255)

    def __str__(self):
        return f"HealthRecord {self.id} for {self.user.username} on {self.record_date}"


class HealthPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="health_plans"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    plan_details = models.TextField()
    valid_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Health Plan #{self.plan_id} for User {self.user_id}"

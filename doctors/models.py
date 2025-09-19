from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

# Create your models here.


class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Doctor(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending Approval"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("suspended", "Suspended"),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True
    )
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField()
    qualification = models.CharField(max_length=200)
    hospital_affiliation = models.CharField(max_length=200, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    biography = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to="doctors/profiles/", blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization.name}"

    class Meta:
        verbose_name = "Doctor Profile"
        verbose_name_plural = "Doctors Profiles"
        ordering = ["user__last_name", "user__first_name"]


class DoctorAvailability(models.Model):
    DAYS_OF_WEEK = (
        ("monday", "Monday"),
        ("tuesday", "Tuesday"),
        ("wednesday", "Wednesday"),
        ("thursday", "Thursday"),
        ("friday", "Friday"),
        ("saturday", "Saturday"),
        ("sunday", "Sunday"),
    )

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="availabilities"
    )
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        return f"{self.doctor.user.get_full_name()} - {self.date} {self.start_time}-{self.end_time} ({status})"

    class Meta:
        unique_together = ("doctor", "day_of_week", "start_time", "end_time")
        ordering = ["day_of_week", "start_time"]

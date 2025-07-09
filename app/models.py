#!/usr/bin/env python3
"""
models.py — Data models for the 'vylety' Django application.

Defines custom user model for registration, event model for scientific excursions,
and application model to store user registrations to events.

This module is intended to be used with Django ORM and supports
automatic admin and form generation. Part of the 'Výlety za vědou' project.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Extends Django's built-in AbstractUser model with additional fields
    relevant to registration for science excursions.

    Attributes:
        dob (DateField): Date of birth of the user.
        street (CharField): Street name of the user's address.
        city (CharField): City of the user's address.
        number (CharField): Street number or apartment number.
        postal_code (CharField): Postal code of the address.
        phone (CharField): Phone number, typically in international format.
        school (CharField): Name of the school the user attends.
        grade (CharField): School grade or year.
        id_number (CharField): National ID or passport number.
    """
    dob = models.DateField()
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    school = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)
    id_number = models.CharField(max_length=20)

class Event(models.Model):
    """
    Represents a science-related event or course that users can register for.

    Attributes:
        name (CharField): Title of the event.
        date (DateField): Date when the event begins.
        description (TextField): Short summary of the event.
        long_description (TextField): Detailed explanation about the event.
        place (CharField): Location where the event takes place.
        age_group (CharField): Target age group (e.g. 15–20).
        target_group (CharField): Target audience (e.g. high school students).
        price_description (TextField): Pricing and donation information.
        food_info (TextField): Information about provided meals.
        to_bring (TextField): Recommended items to bring.
        contact (TextField): Contact details for the event.
        schedule_coming_later (BooleanField): True if schedule will be announced later.
    """
    name = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    long_description = models.TextField()
    place = models.CharField(max_length=200)
    age_group = models.CharField(max_length=50)
    target_group = models.CharField(max_length=100)
    price_description = models.TextField()
    food_info = models.TextField()
    to_bring = models.TextField()
    contact = models.TextField()
    schedule_coming_later = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns the name of the event for display in Django admin or dropdowns.
        """
        return self.name

class Application(models.Model):
    """
    Stores a registration of a user for a particular event.

    Attributes:
        user (ForeignKey): Reference to the user who applies.
        event (ForeignKey): Reference to the event.
        note (TextField): Optional note from the user.
        status (CharField): Status of the application (pending, approved, rejected).

    Meta:
        unique_together: Prevents duplicate applications by same user to same event.
    """
    STATUS_CHOICES = [
        ('pending', 'Čeká'),
        ('approved', 'Schváleno'),
        ('rejected', 'Zamítnuto'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('user', 'event')

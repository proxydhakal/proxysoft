"""
User profile with full_name (used for display in admin/dashboard).
Uses Django's default User; full_name is stored in Profile for "full_name instead of first/last" display.
"""
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Optional profile: full_name for display (instead of first_name + last_name)."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    full_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.full_name or self.user.username

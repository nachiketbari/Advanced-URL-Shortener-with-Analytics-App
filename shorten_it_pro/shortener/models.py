from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Function to generate a random shortcode
import random
import string

def generate_shortcode(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=200)
    short_code = models.CharField(max_length=10, unique=True, default=generate_shortcode)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.original_url} ({self.short_code})"

class URLAnalytics(models.Model):
    shortened_url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE, related_name='analytics')
    access_time = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()

    def __str__(self):
        return f"Analytics for {self.shortened_url.short_code} at {self.access_time}"

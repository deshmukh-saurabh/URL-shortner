from django.db import models


class URL(models.Model):
    hash = models.TextField(unique=True)
    original_url = models.TextField()
    expiration_ts = models.DateTimeField(blank=True, null=True)
    expired = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "URL"
        verbose_name_plural = "URLs"
    
    def __str__(self):
        return str(self.id)

    

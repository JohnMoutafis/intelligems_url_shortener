from django.db import models


class AvailableUrls(models.Model):
    """
    A model of the available urls in the database.
    """
    url = models.CharField(max_length=40, null=False, unique=True)
    in_use = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Available URL'
        verbose_name_plural = 'Available URLs'


class ShortenedUrls(models.Model):
    """
    A model representing the shortened urls.
    """
    initial_url = models.URLField(unique=True)
    shortened_url = models.ForeignKey(
        AvailableUrls, related_name='short_url', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Shortened URL'
        verbose_name_plural = 'Shortened URLs'

    def save(self, *args, **kwargs):
        """
        On save, update the shortened_url's `in_use` field to True.
        """
        instance = super().save(*args, **kwargs)
        self.shortened_url.in_use = True
        self.shortened_url.save()
        return instance

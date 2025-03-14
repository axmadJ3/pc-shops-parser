from django.db import models


class Product(models.Model):
    site = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    url = models.URLField(max_length=500, unique=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        unique_together = ('site', 'name')

    def __str__(self):
        return f'{self.name} ({self.site})'

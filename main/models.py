from django.db import models


class Product(models.Model):
    site = models.CharField(max_length=255, verbose_name='Sayt', db_index=True)
    name = models.CharField(max_length=255, verbose_name='Noutbuk nomi', db_index=True)
    price = models.IntegerField(verbose_name='Narxi')
    url = models.URLField(max_length=500, unique=True, verbose_name='URL')
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='Rasm URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    updated_at = models.DateTimeField(auto_now=True, verbose_name="O'zgartirilgan vaqt")

    class Meta:
        db_table = 'products'
        verbose_name = 'Noutbuk'
        verbose_name_plural = 'Noutbuklar'
        unique_together = ('url', 'name')

    def __str__(self):
        return f'{self.name} ({self.site})'

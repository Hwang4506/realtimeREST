from django.db import models
from django.utils import timezone

class Realbar(models.Model):
    barcode = models.CharField(max_length=50)
    create_date = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.barcode

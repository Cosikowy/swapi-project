from django.db import models


class Collection(models.Model):
    id = models.UUIDField("Collection ID")
    file_name = models.CharField("File Name", max_length=72)
    file_location = models.TextField("File Location")
    timestamp = models.DateTimeField(
        verbose_name="Download timestamp", auto_now_add=True
    )

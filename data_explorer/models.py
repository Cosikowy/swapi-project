import os

from django.db import models


class Collection(models.Model):
    id = models.UUIDField("Collection ID", primary_key=True)
    file_name = models.CharField("File Name", max_length=72)
    file_location = models.TextField("File Location")
    timestamp = models.DateTimeField(
        verbose_name="Download timestamp", auto_now_add=True
    )
    etag = models.CharField("Version tag", max_length=80)
    endpoint = models.CharField("Endpoint", max_length=50)

    def __str__(self) -> str:
        return f"{self.endpoint} {self.id}"

    @property
    def full_path(self):
        return os.path.join(self.file_location, self.file_name)

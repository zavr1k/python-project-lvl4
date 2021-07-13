from django.db import models


class TaskStatus(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
    )
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

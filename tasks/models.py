from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TaskStatus(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
    )
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Task status')
        verbose_name_plural = _('Task statuses')


class Task(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    status = models.ForeignKey('TaskStatus', on_delete=models.RESTRICT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='author',
                               on_delete=models.RESTRICT)
    executor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='executor',
                                 on_delete=models.RESTRICT)
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.title

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    status = models.ForeignKey('statuses.Status', on_delete=models.RESTRICT)
    labels = models.ManyToManyField('Label', blank=True, related_name='tasks')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='author',
                               on_delete=models.RESTRICT)
    executor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='executor',
                                 on_delete=models.RESTRICT)
    time_create = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        verbose_name = _('Задача')
        verbose_name_plural = _('Задачи')

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=255, unique=True)
    time_create = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Метка')
        verbose_name_plural = _('Метки')

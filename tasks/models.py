from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import TaskUser
from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=255,
                            unique=True)

    description = models.TextField(blank=True)
    status = models.ForeignKey(Status,
                               on_delete=models.RESTRICT)
    labels = models.ManyToManyField('Label',
                                    blank=True,
                                    related_name='tasks')
    author = models.ForeignKey(TaskUser,
                               related_name='author',
                               on_delete=models.RESTRICT)
    executor = models.ForeignKey(TaskUser,
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

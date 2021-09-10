from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=255, unique=True)
    time_create = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Метка')
        verbose_name_plural = _('Метки')

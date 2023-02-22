from django.db import models


class CreateModel(models.Model):
    created = models.DateTimeField(verbose_name='Дата создания',
                                   auto_now_add=True)

    class Meta:
        abstract = True

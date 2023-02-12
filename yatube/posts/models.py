from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(verbose_name='Адрес', unique=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Тело поста')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата создания')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='post',
                               verbose_name='Автор')
    group = models.ForeignKey(Group,
                              on_delete=models.SET_NULL,
                              blank=True, null=True,
                              verbose_name='Группа',
                              related_name='post')

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ('pub_date',)

from django.db import models

from django.contrib.auth import get_user_model

from core.models import CreateModel

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
    image = models.ImageField(verbose_name='Картнка',
                              upload_to='posts/',
                              blank=True)

    def __str__(self):
        return self.text[:15]

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='Пост')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор')
    text = models.TextField(verbose_name='Тело коммента',
                            help_text='Введите текст')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания')

    class Meta:
        ordering = ["-created"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name='Фолловер',
                             related_name='follower'
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Фолловинг',
                               related_name='following'
                               )

    class Meta:
        verbose_name = "Подписаться на автора"
        verbose_name_plural = "Подписки"
        models.UniqueConstraint(fields=["user", "author"], name="following")

    def __str__(self):
        return f"Подписка {self.user} на {self.author}"

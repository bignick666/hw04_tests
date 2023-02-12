from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from ..forms import PostForm
from ..models import Post, Group, User


class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.authorized_client = Client()
        cls.user = User.objects.create_user(username='Geek')
        cls.authorized_client.force_login(cls.user)
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый постик',
        )
        # Создаем форму, если нужна проверка атрибутов

    def test_post_create(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовая запись новая',
            'author': self.post.author,
        }
        response = self.authorized_client.post(reverse('posts:create'),
                                               data=form_data,
                                               follow=True,
                                               )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, reverse('posts:profile',
                                               kwargs={'username': self.user.username}))

    def test_post_edit(self):
        group = Group.objects.create(
            title='Тестовая группа_2',
            slug='test_slug',
            description='Just a test group'
        )
        post = Post.objects.create(
            author=self.user,
            text='testovii post',
            group=group
        )
        url = reverse('posts:post_edit', kwargs={"post_id": post.id})
        self.response = self.authorized_client.post(url, {
            "text": "Обновленный пост",
            "group": group.id,
        })
        post.refresh_from_db()
        self.assertEqual(post.text, "Обновленный пост")
        self.assertEqual(post.group.id, group.id)


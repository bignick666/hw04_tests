from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group, User

from posts.tests.constants import POSTS_PROFILE,\
    POSTS_EDIT, POSTS_CREATE


class PostCreateFormTests(TestCase):
    def setUp(self):
        self.authorized_client = Client()
        self.user = User.objects.create_user(username='Geek')
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый постик',
        )

    def test_post_create(self):
        """Тест формы создания поста"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовая запись новая',
            'author': self.post.author,
        }
        response = self.authorized_client.post(
            reverse(POSTS_CREATE),
            data=form_data,
            follow=True,
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(
            response,
            reverse(POSTS_PROFILE,
                    kwargs={'username': self.user.username}))

    def test_post_edit(self):
        """Тест формы редактирования поста"""
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
        url = reverse(POSTS_EDIT,
                      kwargs={"post_id": post.id})
        self.response = self.authorized_client.post(url, {
            "text": "Обновленный пост",
            "group": group.id,
        })
        post.refresh_from_db()
        self.assertEqual(post.text, "Обновленный пост")
        self.assertEqual(post.group, group)

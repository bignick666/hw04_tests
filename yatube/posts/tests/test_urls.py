from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User
from posts.tests.constants import POSTS_PROFILE,\
    POSTS_EDIT, POSTS_CREATE, POSTS_INDEX,\
    POSTS_GROUPS, POSTS_DETAIL, UNEXPECTED_PAGE


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.authorized_client = Client()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Geek')
        cls.authorized_client.force_login(cls.user)
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый постик'
        )
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
        )

    def test_homepage(self):
        # Отправляем запрос через client,
        # созданный в setUp()
        response = self.guest_client.get(reverse(POSTS_INDEX))
        self.assertEqual(response.status_code, 200)

    def test_grouppage(self):
        response = self.guest_client.get(
            reverse(POSTS_GROUPS, kwargs={'slug': 'test-slug'})
        )
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.guest_client.get(
            reverse(POSTS_PROFILE, kwargs={'username': 'Geek'})
        )
        self.assertEqual(response.status_code, 200)

    def test_posts(self):
        response = self.guest_client.get(
            reverse(POSTS_DETAIL, kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_posts_edit(self):
        response = self.authorized_client.get(
            reverse(POSTS_EDIT, kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_createpage(self):
        response = self.authorized_client.get(reverse(POSTS_CREATE))
        self.assertEqual(response.status_code, 200)

    def test_unexpectedpage(self):
        response = self.guest_client.get(UNEXPECTED_PAGE)
        self.assertEqual(response.status_code, 404)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            reverse(POSTS_INDEX): 'posts/index.html',
            reverse(POSTS_GROUPS,
                    kwargs={'slug': 'test-slug'}
                    ): 'posts/group_list.html',
            reverse(POSTS_PROFILE,
                    kwargs={'username': 'Geek'}
                    ): 'posts/profile.html',
            reverse(POSTS_DETAIL,
                    kwargs={'post_id': self.post.id}
                    ): 'posts/post_detail.html',
            reverse(POSTS_CREATE): 'posts/create.html'

        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

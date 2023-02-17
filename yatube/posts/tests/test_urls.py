from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User
from posts.tests.constants import PROFILE_URL,\
    INDEX_URL, CREATE_URL,\
    GROUPS_URL, DETAIL_URL, EDIT_URL, UNEXPECTED_PAGE,\
    PROFILE_TEMPLATE, INDEX_TEMPLATE,\
    CREATE_TEMPLATE, GROUPS_TEMPLATE, DETAIL_TEMPLATE


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='Geek')

    def setUp(self):
        self.authorized_client = Client()
        self.guest_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый постик'
        )
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
        )

    def test_homepage(self):
        response = self.guest_client.get(reverse(INDEX_URL))
        self.assertEqual(response.status_code, 200)

    def test_grouppage(self):
        response = self.guest_client.get(
            reverse(GROUPS_URL, kwargs={'slug': 'test-slug'})
        )
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        response = self.guest_client.get(
            reverse(PROFILE_URL, kwargs={'username': 'Geek'})
        )
        self.assertEqual(response.status_code, 200)

    def test_posts(self):
        response = self.guest_client.get(
            reverse(DETAIL_URL, kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_posts_edit(self):
        response = self.authorized_client.get(
            reverse(EDIT_URL, kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_createpage(self):
        response = self.authorized_client.get(reverse(CREATE_URL))
        self.assertEqual(response.status_code, 200)

    def test_unexpectedpage(self):
        response = self.guest_client.get(UNEXPECTED_PAGE)
        self.assertEqual(response.status_code, 404)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            reverse(INDEX_URL): INDEX_TEMPLATE,
            reverse(GROUPS_URL,
                    kwargs={'slug': 'test-slug'}
                    ): GROUPS_TEMPLATE,
            reverse(PROFILE_URL,
                    kwargs={'username': 'Geek'}
                    ): PROFILE_TEMPLATE,
            reverse(DETAIL_URL,
                    kwargs={'post_id': self.post.id}
                    ): DETAIL_TEMPLATE,
            reverse(CREATE_URL): CREATE_TEMPLATE

        }
        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

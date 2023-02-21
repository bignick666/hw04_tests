from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group, User
from posts.utils import POSTS_PER_PAGE
from posts.tests.constants import PROFILE_URL,\
    INDEX_URL, CREATE_URL,\
    GROUPS_URL, DETAIL_URL, EDIT_URL,\
    PROFILE_TEMPLATE, INDEX_TEMPLATE,\
    CREATE_TEMPLATE, GROUPS_TEMPLATE, DETAIL_TEMPLATE

from posts.forms import PostForm

TEST_POSTS_ALL = 13
TEST_POSTS_SECOND_PAGE = TEST_POSTS_ALL - POSTS_PER_PAGE


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
            text='Тестовый постик',
        )
        self.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
        )

    def test_urls_uses_correct_template(self):
        templates_page_names = {
            reverse(INDEX_URL): INDEX_TEMPLATE,
            reverse(CREATE_URL): CREATE_TEMPLATE,
            reverse(GROUPS_URL,
                    kwargs={'slug': 'test-slug'}): GROUPS_TEMPLATE,
            reverse(PROFILE_URL,
                    kwargs={'username': 'Geek'}): PROFILE_TEMPLATE,
            reverse(DETAIL_URL,
                    kwargs={'post_id': 1}): DETAIL_TEMPLATE,
            reverse(EDIT_URL,
                    kwargs={'post_id': 1}): CREATE_TEMPLATE
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_create_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(CREATE_URL))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_detail_page_show_correct_context(self):
        response = self.guest_client.get(
            reverse(DETAIL_URL, kwargs={'post_id': 1})
        )
        self.assertEqual(response.context['post'].author,
                         self.post.author)
        self.assertEqual(response.context['post'].text,
                         'Тестовый постик')
        self.assertEqual(response.context['post'].image,
                         self.post.image)
        self.assertEqual(response.context['author_posts_count'].count(),
                         1)
        self.assertEqual(response.context['post'].pub_date,
                         self.post.pub_date)
        self.assertEqual(response.context['post'].group,
                         self.post.group)

    def test_post_edit_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(EDIT_URL, kwargs={"post_id": self.post.id})
        )
        form_fields = {
            "text": forms.fields.CharField,
            "group": forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form = response.context.get('form')
                self.assertIsInstance(form, PostForm)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(PROFILE_URL, kwargs={'username': 'Geek'}))
        test_profile_username = response.context['profile']
        test_object_post = response.context["page_obj"][0]
        self.assertEqual(test_profile_username, self.post.author)
        self.assertEqual(test_object_post.image, self.post.image)

    def test_group_list_page_show_correct_context(self):
        self.post = Post.objects.create(
            author=self.user,
            text='Тестовый постик1',
            group=self.group
        )
        response = self.guest_client.get(
            reverse(GROUPS_URL, kwargs={'slug': 'test-slug'})
        )
        test_group_title = response.context['group'].title
        test_group_description = response.context['group'].description
        test_object_post = response.context["page_obj"][0]
        self.assertEqual(test_object_post.text, "Тестовый постик1")
        self.assertEqual(test_object_post.author.username, "Geek")
        self.assertEqual(test_object_post.image, self.post.image)

        self.assertEqual(test_group_title, self.group.title)
        self.assertEqual(test_group_description,
                         self.group.description)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(INDEX_URL))
        test_object_post = response.context["page_obj"][0]
        self.assertEqual(test_object_post.text, "Тестовый постик")
        self.assertEqual(test_object_post.author.username, "Geek")
        self.assertEqual(test_object_post.group, self.post.group)
        self.assertEqual(test_object_post.image, self.post.image)

    def test_post_in_index(self):
        self.post2 = Post.objects.create(
            author=self.user,
            group=self.group,
            text='Description text'
        )

        response_index = self.authorized_client.get(
            reverse(INDEX_URL))
        test_object_index = response_index.context["page_obj"][1]
        self.assertEqual(test_object_index.text, "Description text")
        self.assertEqual(test_object_index.author.username, "Geek")
        self.assertEqual(test_object_index.group, self.group)

        response_group_list = self.authorized_client.get(reverse(
            GROUPS_URL,
            kwargs={'slug': 'test-slug'}))
        test_object_group = response_group_list.context["page_obj"][0]
        self.assertEqual(test_object_group.text, "Description text")
        self.assertEqual(test_object_group.author.username, "Geek")

        response_profile = self.authorized_client.get(reverse(
            PROFILE_URL,
            kwargs={'username': 'Geek'}
        ))
        test_object_profile = response_profile.context['page_obj'][1]
        self.assertEqual(test_object_profile.text, "Description text")
        self.assertEqual(test_object_profile.author.username, "Geek")


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username="Geek")
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title="test_title",
            slug="test_slug",
            description="test_description",
        )
        test_post = []
        for post in range(TEST_POSTS_ALL):
            Post.objects.create(
                author=cls.user,
                group=cls.group,
                text=f'Тестовый пост №{post}'
            )
            test_post.append(post)

    def test_first_page_contains_ten_records(self):
        response = self.authorized_client.get(
            reverse(INDEX_URL))
        self.assertEqual(len(response.context['page_obj']), POSTS_PER_PAGE)

    def test_second_page_contains_three_records(self):
        response = self.authorized_client.get(
            reverse(INDEX_URL) + '?page=2')
        self.assertEqual(len(response.context['page_obj']),
                         TEST_POSTS_SECOND_PAGE)

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_post_have_correct_object_name(self):
        post = PostModelTest.post
        expected_name = post.text[:15]
        self.assertEqual(expected_name, str(post))

    def test_models_group_have_correct_object_name(self):
        group = PostModelTest.group
        expected_name = group.title
        self.assertEqual(expected_name, str(group))

    def test_models_group_verbose_names(self):
        group = PostModelTest.group
        field_verboses = {
            'title': 'Название',
            'slug': 'Адрес',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(group._meta.get_field(value).verbose_name, expected)

    def test_models_post_verbose_names(self):
        post = PostModelTest.post
        field_verboses = {
            'text': 'Тело поста',
            'pub_date': 'Дата создания',
            'author': 'Автор',
            'group': 'Группа'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(post._meta.get_field(value).verbose_name, expected)
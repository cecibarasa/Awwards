from django.test import TestCase
from .models import *


class TestProfile(TestCase):
    def setUp(self):
        self.user = User(id=1, username='cecilia', password='1738')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()


class ProjectTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='cecilia')
        self.post = Project.objects.create(id=1, title='test post', image='https://ucarecdn.com/0ccf61ff-508e-46c6-b713-db51daa6626e', details='desc',
                                        user=self.user, link='http://ur.coml')

    def test_instance(self):
        self.assertTrue(isinstance(self.post, Project))

    def test_save_post(self):
        self.post.save_post()
        post = Project.objects.all()
        self.assertTrue(len(post) > 0)

    def test_get_posts(self):
        self.post.save()
        posts = Project.fetch_all_images()
        self.assertTrue(len(posts) > 0)

    def test_search_post(self):
        self.post.save()
        post = Project.search_project_by_title('test')
        self.assertTrue(len(post) > 0)

    def test_delete_post(self):
        self.post.delete_post()
        post = Project.search_project_by_title('test')
        self.assertTrue(len(post) < 1)


class RateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(id=1, username='cecilia')
        self.post = Project.objects.create(id=1, title='test post', image='https://ucarecdn.com/0ccf61ff-508e-46c6-b713-db51daa6626e', details='desc',
                                        user=self.user, link='http://ur.coml')
        self.rating = Rate.objects.create(id=1, design=6, usability=7, creativity=9, content=9, user=self.user, post=self.post)

    def test_instance(self):
        self.assertTrue(isinstance(self.rating, Rate))

    def test_save_rating(self):
        self.rating.save_rate()
        rating = Rate.objects.all()
        self.assertTrue(len(rating) > 0)

    # def test_get_post_rating(self, id):
    #     self.rating.save()
    #     rating = Rate.get_ratings(post_id=id)
    #     self.assertTrue(len(rating) == 1)

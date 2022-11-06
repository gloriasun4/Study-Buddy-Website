# Source: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class MakePostViewTest(TestCase):
    def setUp(self):
        self.test_email = 'test@email.com'
        self.test_username = 'testName'
        self.test_password = 'testPassword'
        self.test_dept = 'testDept'
        self.test_course_number = 12345

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    # def test_view_url_exists_at_desired_location(self):
    #     """
    #     url is valid to make a post
    #
    #     Source for "follow=True" - https://stackoverflow.com/questions/21215035/django-test-always-returning-301
    #     """
    #     response = self.client.get(('/studybuddy/', self.test_subject, '/', self.test_course_number, '/makepost'),
    #                                 follow=True)
    #     self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        makepost view is accessible through its name
        """
        response = self.client.get(reverse('studybuddy:makepost', args=(self.test_email,
                                                                        self.test_dept,
                                                                        self.test_course_number)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        makepost view uses the correct template
        """
        response = self.client.get(reverse('studybuddy:makepost', args=(self.test_email,
                                                                        self.test_dept,
                                                                        self.test_course_number)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/makepost.html')

class SubmitPostViewTest(TestCase):
    def setUp(self):
        self.test_email = 'test@email.com'
        self.test_username = 'testName'
        self.test_password = 'testPassword'
        self.test_dept = 'testDept'
        self.test_course_number = 12345

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    # def test_view_url_exists_at_desired_location(self):
    #     """
    #     url is valid to submit a post
    #
    #     Source for "follow=True" - https://stackoverflow.com/questions/21215035/django-test-always-returning-301
    #     """
    #     response = self.client.get(('/studybuddy/', self.test_subject, '/', self.test_course_number, '/submitpost'),
    #                                 follow=True)
    #     self.assertEqual(response.status_code, 200)

    def test_url_accessible_by_name(self):
        """
        submit post is accessible through its name and will be redirected to coursefeed
        """
        response = self.client.get(reverse('studybuddy:submitpost', args=(self.test_email,
                                                                        self.test_dept,
                                                                        self.test_course_number)))
        # OH: why is this a 302 instead of a 301?
        self.assertEqual(response.status_code, 302)

    def test_view_uses_correct_template(self):
        """
        submitpost uses the correct template
        """
        response = self.client.get(reverse('studybuddy:makepost', args=(self.test_email,
                                                                        self.test_dept,
                                                                        self.test_course_number)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/makepost.html')

class ViewPostViewTest(TestCase):
    def setUp(self):
        self.test_email = 'test@email.com'
        self.test_username = 'testName'
        self.test_password = 'testPassword'

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    def test_view_url_exists_at_desired_location(self):
        """
        url is valid for user to view their posts

        Source for "follow=True" - https://stackoverflow.com/questions/21215035/django-test-always-returning-301
        """
        response = self.client.get('/studybuddy/viewposts', follow=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('studybuddy.models.User.objects')
    def test_view_url_accessible_by_name(self, mock_user):
        """
        viewposts view is accessible through its name
        """
        # given
        mock_user.get.return_value = mock_user

        # when
        response = self.client.get(reverse('studybuddy:viewposts'))

        # then
        self.assertEqual(response.status_code, 200)

    @mock.patch('studybuddy.models.User.objects')
    def test_view_uses_correct_template(self, mock_user):
        """
        viewposts view uses the correct template
        """
        # given
        mock_user.get.return_value = mock_user

        # when
        response = self.client.get(reverse('studybuddy:viewposts'))

        # then
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/viewposts.html')
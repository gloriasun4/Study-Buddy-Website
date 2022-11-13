from unittest import mock
from django.urls import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from studybuddy.models import User
from studybuddy.views.friend_views import view_friends


class FriendViewTest(TestCase):
    def setUp(self):
        self.test_email = 'test@email.com'
        self.test_username = 'testName'
        self.test_password = 'testPassword'
        self.test_friend_email = 'testFriend@email.com'

        User.objects.create(email=self.test_email)
        self.test_request_factory = RequestFactory()

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    def test_view_url_exists_at_desired_location(self):
        """
        url is valid to view friends and friend requests

        Source for "follow=True" - https://stackoverflow.com/questions/21215035/django-test-always-returning-301
        """
        response = self.client.get('/studybuddy/friends', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        view friends view is accessible through its name
        """
        response = self.client.get(reverse('studybuddy:viewFriends'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        view friends view uses the correct template
        """
        response = self.client.get(reverse('studybuddy:viewFriends'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friends/view_friends.html')

    @mock.patch('studybuddy.views.friend_views.accept_friend_request')
    def test_accept_calls_method(self, mock_accept_friend_request):
        """
        when a user accepts a friend request, the accept method is called
        """
        # given
        test_view_accept_friend_request = self.test_request_factory.post(
            '/studybuddy/friends', {'accept': 'accept',
                                    'ad_email': self.test_friend_email})
        test_view_accept_friend_request.user = self.test_user

        # when
        response = view_friends(test_view_accept_friend_request)

        # then
        self.assertEqual(response.status_code, 200)
        mock_accept_friend_request.assert_called_once_with(test_view_accept_friend_request, self.test_friend_email)

    @mock.patch('studybuddy.views.friend_views.decline_request')
    def test_decline_calls_method(self, mock_decline_request):
        """
        when a user decline a friend request, the decline method is called
        """
        # given
        test_view_decline_friend_request = self.test_request_factory.post(
            '/studybuddy/friends', {'decline': 'decline',
                                    'ad_email': self.test_friend_email})
        test_view_decline_friend_request.user = self.test_user

        # when
        response = view_friends(test_view_decline_friend_request)

        # then
        self.assertEqual(response.status_code, 200)
        mock_decline_request.assert_called_once_with(test_view_decline_friend_request, self.test_friend_email)

    @mock.patch('studybuddy.views.friend_views.remove_friend')
    def test_remove_calls_method(self, mock_remove_friend):
        """
        when a user removes a friend, the remove method is called
        """
        # given
        test_view_remove_friend_request = self.test_request_factory.post(
            '/studybuddy/friends', {'unfriend': 'unfriend',
                                    'remove_email': self.test_friend_email})
        test_view_remove_friend_request.user = self.test_user

        # when
        response = view_friends(test_view_remove_friend_request)

        # then
        self.assertEqual(response.status_code, 200)
        mock_remove_friend.assert_called_once_with(test_view_remove_friend_request, self.test_friend_email)
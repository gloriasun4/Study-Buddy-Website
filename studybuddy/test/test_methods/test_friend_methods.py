from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model

from studybuddy.models import User, Friend_Request
from studybuddy.views.friend_views import accept_friend_request, decline_request


class FriendActionTests(TestCase):
    def setUp(self):
        self.test_email = 'test@email.com'
        self.test_username = 'testName'
        self.test_username2 = 'testFriendName'
        self.test_password = 'testPassword'
        self.test_password2 = 'testFriendPassword'
        self.test_friend_email = 'testFriend@email.com'

        self.test_request_factory = RequestFactory()
        self.test_user1 = User.objects.create(email=self.test_email)
        self.test_user2 = User.objects.create(email=self.test_friend_email)

        Friend_Request.objects.create(to_user=self.test_user2, from_user=self.test_user1)

        self.test_user1 = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.test_user2 = get_user_model().objects.create_user(self.test_username2, self.test_friend_email, self.test_password2)

    # def test_accept_adds_friend(self):
    #     """
    #     when a user accepts a friend request, the user is added to each other's friend list
    #     """
    #     # given
    #     test_view_accept_friend_request = self.test_request_factory.post(
    #         '/studybuddy/friends', {'accept': 'accept',
    #                                 'ad_email': self.test_email})
    #     test_view_accept_friend_request.user = self.test_user2
    #
    #     # when
    #     print(Friend_Request.objects.all())
    #     accept_friend_request(test_view_accept_friend_request, self.test_email)
    #     print('friends: ', User.objects.get(email=self.test_email).friends)
    #
    #     # then
    #     self.assertEqual(User.objects.get(email=self.test_email).friends.filter(self.test_friend_email).exists(), True)
    #
    # def test_decline_removes_friend_request(self):
    #     """
    #     when a user declines a friend request, the friend request is removed
    #     """
    #     # given
    #     test_view_decline_friend_request = self.test_request_factory.post(
    #         '/studybuddy/friends', {'decline': 'decline',
    #                                 'ad_email': self.test_friend_email})
    #     test_view_decline_friend_request.user = self.test_user2
    #
    #     self.assertEqual(Friend_Request.objects.filter(to_user=self.test_friend_email).count(), 1)
    #
    #     # when
    #     decline_request(test_view_decline_friend_request, self.test_friend_email)
    #
    #     # then
    #     self.assertEqual(Friend_Request.objects.filter(to_user=self.test_friend_email).count(), 0)

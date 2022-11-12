# from django.urls import reverse
# from django.test import TestCase
# from django.contrib.auth import get_user_model
# from studybuddy.models import User
#
#
# class FriendViewTest(TestCase):
#     def setUp(self):
#         self.test_email = 'test@email.com'
#         self.test_username = 'testName'
#         self.test_password = 'testPassword'
#
#         User.objects.create(email=self.test_email)
#
#         # mock user login
#         self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
#         self.client.login(username=self.test_username, password=self.test_password)
#
#     def test_view_url_exists_at_desired_location(self):
#         """
#         url is valid to view friends and friend requests
#
#         Source for "follow=True" - https://stackoverflow.com/questions/21215035/django-test-always-returning-301
#         """
#         response = self.client.get('/studybuddy/friends', follow=True)
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_url_accessible_by_name(self):
#         """
#         view friends view is accessible through its name
#         """
#         response = self.client.get(reverse('studybuddy:viewFriends'))
#         self.assertEqual(response.status_code, 200)
#
#     def test_view_uses_correct_template(self):
#         """
#         view friends view uses the correct template
#         """
#         response = self.client.get(reverse('studybuddy:viewFriends'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'friends/view_friends.html')
from unittest import mock
from django.urls import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from studybuddy.models import Room, User, StudySession
from studybuddy.views.study_session_views import upcomingSessions


class ScheduleViewTest(TestCase):
    def setUp(self):
        self.test_email = 'test@email.com'
        self.test_username = 'testName'
        self.test_password = 'testPassword'
        self.test_room = 'testRoom'

        Room.objects.create(name=self.test_room, slug=self.test_room)

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    def test_view_url_exists_at_desired_location(self):
        """
        url is valid to schedule a study session

        Source for "follow=True" - https://stackoverflow.com/questions/21215035/django-test-always-returning-301
        """
        response = self.client.get('/studybuddy/' + self.test_room + '/schedule', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        schedule view is accessible through its name
        """
        response = self.client.get(reverse('studybuddy:schedule', args=(self.test_room,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        schedule view uses the correct template
        """
        response = self.client.get(reverse('studybuddy:schedule', args=(self.test_room,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule_sessions/schedule.html')

    def test_displays_scheduling_form(self):
        """
        upcoming study session can be booked for a room
        """
        response = self.client.get(reverse('studybuddy:schedule', args=(self.test_room,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Schedule a study session for: ' + self.test_room)

    def test_displays_message_when_room_is_not_valid(self):
        """
        when room is not valid, appropriate message is displayed
        """
        # given
        Room.objects.all().delete()

        # when
        response = self.client.get(reverse('studybuddy:schedule', args=(self.test_room,)))

        # then
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Room ' + self.test_room + ' does not exist')


class UpcomingSessionsViewTest(TestCase):
    def setUp(self):
        self.test_email = 'test@email.com'
        self.test_username = 'testName'
        self.test_password = 'testPassword'
        self.test_study_session_name = 'testStudySession'
        self.test_date = '2023-01-01'
        self.start = '01:30'
        self.end = '2:30'
        self.test_accepted = '?'
        self.test_room = 'testRoom'

        self.test_request_factory = RequestFactory()
        User.objects.create(email=self.test_email)

        StudySession.objects.create(name=self.test_study_session_name,
                                    date=self.test_date,
                                    start=self.start,
                                    end=self.end,
                                    accepted=self.test_accepted)

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    def test_view_url_exists_at_desired_location(self):
        """
        url is valid to view upcoming study sessions

        Source for "follow=True" - https://stackoverflow.com/questions/21215035/django-test-always-returning-301
        """
        response = self.client.get('/studybuddy/upcomingSessions', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        upcomingSessions is accessible through its name
        """
        response = self.client.get(reverse('studybuddy:upcomingSessions'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        upcomingSessions uses the correct template
        """
        response = self.client.get(reverse('studybuddy:upcomingSessions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'schedule_sessions/upcomingSessions.html')

    @mock.patch('studybuddy.views.study_session_views.acceptSession')
    def test_accept_calls_method(self, mock_acceptSession):
        """
        when a user accepts a study session, the accept method is called
        """
        # given
        test_view_accept_session_request = self.test_request_factory.post(
            '/studybuddy/upcomingSessions', {'accept': 'accept',
                                             'session_pk': 1})
        test_view_accept_session_request.user = self.test_user

        # when
        response = upcomingSessions(test_view_accept_session_request)

        # then
        self.assertEqual(response.status_code, 200)
        mock_acceptSession.assert_called_once_with(test_view_accept_session_request)

    @mock.patch('studybuddy.views.study_session_views.declineSession')
    def test_decline_calls_method(self, mock_declineSession):
        """
        when a user declines a study session, the decline method is called
        """
        # given
        test_view_decline_session_request = self.test_request_factory.post(
            '/studybuddy/upcomingSessions', {'decline': 'decline',
                                             'session_pk': 1})
        test_view_decline_session_request.user = self.test_user

        # when
        response = upcomingSessions(test_view_decline_session_request)

        # then
        self.assertEqual(response.status_code, 200)
        mock_declineSession.assert_called_once_with(test_view_decline_session_request)

    @mock.patch('studybuddy.views.study_session_views.deleteSession')
    def test_delete_calls_method(self, mock_deleteSession):
        """
        when a user declines a study session, the decline method is called
        """
        # given
        test_view_delete_session_request = self.test_request_factory.post(
            '/studybuddy/upcomingSessions', {'delete': 'delete',
                                             'session_pk': 1})
        test_view_delete_session_request.user = self.test_user

        # when
        response = upcomingSessions(test_view_delete_session_request)

        # then
        self.assertEqual(response.status_code, 200)
        mock_deleteSession.assert_called_once_with(test_view_delete_session_request)

    def test_schedule_creates_study_session(self):
        """
        when a user schedules a study session, the study session is added
        """
        # given
        StudySession.objects.all().delete()
        Room.objects.create(name=self.test_room, slug=self.test_room)

        test_view_schedule_session_request = self.test_request_factory.post(
            '/studybuddy/upcomingSessions', {'schedule' : 'schedule',
                                             'date' : self.test_date,
                                             'start' : self.start,
                                             'end' : self.end,
                                             'roomName' : self.test_room})
        test_view_schedule_session_request.user = self.test_user

        self.assertEqual(StudySession.objects.count(), 0)

        # when
        response = upcomingSessions(test_view_schedule_session_request)

        # then
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudySession.objects.count(), 1)

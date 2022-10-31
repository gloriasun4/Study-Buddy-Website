# Source: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing

from django.test import TestCase
from studybuddy.models import User, Course
from django.urls import reverse
from studybuddy import views
from django.contrib import auth
from unittest.mock import MagicMock
import test
from django.contrib.auth import get_user_model

class CourseFeedViewTest(TestCase):
    def setUp(self):
        self.test_username = 'testName'
        self.test_password = 'testPassword'
        self.test_email = 'test@email.com'
        self.test_subject = 'testDept'
        self.test_catalog_number = 1234
        self.test_instructor = 'testInstructor'
        self.test_section = 000
        self.test_course_number = 12345

        # Course.objects.create(subject=self.test_subject,
        #                       catalog_number=self.test_catalog_number,
        #                       instructor=self.test_instructor,
        #                       section=self.test_section,
        #                       course_number=self.test_course_number)

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    def test_view_url_accessible_by_name(self):
        """
        coursefeed view is accessible through its name
        """
        response = self.client.get(reverse('studybuddy:department', args = (self.test_email, self.test_subject,)))
        self.assertEqual(response.status_code, 200)

    def test_invalid_course_id(self):
        """
        If a course_number is not in the api, an appropiate message is displayed
        """
        response = self.client.get(
            reverse('studybuddy:coursefeed', args = (self.test_email, self.test_subject, self.test_course_number)))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "The department " + self.test_subject.upper() + " you are looking does not exist "
                            "or course number " + str(self.test_course_number) + " in " + self.test_subject.upper() + " is "
                            "not valid.")

    def test_view_uses_correct_template(self):
        """
        coursefeed view uses the correct template
        """
        response = self.client.get(
            reverse('studybuddy:coursefeed', args = (self.test_email, self.test_subject, self.test_course_number)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course_feed.html')

class AllDepartmentViewTest(TestCase):
    def setUp(self):
        self.test_username = 'testName'
        self.test_password = 'testPassword'
        self.test_email = 'test@email.com'

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    def test_view_url_exists_at_desired_location(self):
        """
        url is valid to view all the departments
        """
        response = self.client.get('/studybuddy/alldepartments/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        alldepartments view is accessible through its name
        """
        response = self.client.get(reverse('studybuddy:alldepartments', args = (self.test_email, )))

        # print(reverse('studybuddy:index', args = (self.test_email, )))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        alldepartments view uses the correct template
        """
        response = self.client.get(reverse('studybuddy:alldepartments', args = (self.test_email, )))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'alldepartments.html')

class DepartmentViewTest(TestCase):
    def setUp(self):
        self.test_dept = 'testDept'
        self.test_username = 'testName'
        self.test_password = 'testPassword'
        self.test_email = 'test@email.com'

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    def test_no_courses(self):
        """
        If no courses exist, an appropriate message is displayed.
        **this most likely will occur if the department id is incorrect
        """
        response = self.client.get(reverse('studybuddy:department', args = (self.test_email, self.test_dept,)))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No classes are available in " + self.test_dept.upper() + " or " +
                            self.test_dept.upper() + " does not exist.")

    def test_view_url_accessible_by_name(self):
        """
        department view is accessible through its name
        """
        response = self.client.get(reverse('studybuddy:department', args = (self.test_email, self.test_dept,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        department view uses the correct template
        """
        response = self.client.get(reverse('studybuddy:department', args = (self.test_email, self.test_dept,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'department.html')
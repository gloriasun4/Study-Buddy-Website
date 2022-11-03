# Source: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
import datetime
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from studybuddy.views import views
from django.contrib.auth import get_user_model
from studybuddy.models import Departments, User, Course, Post

class HomepageViewTest(TestCase):
    def setUp(self):
        self.test_email = 'test@email.com'
        self.test_username = 'testName'
        self.test_password = 'testPassword'

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    def test_after_login_redirect_to_homepage(self):
        """
        after user has successfully done google login, they will be redirected to the homepage
        """
        response = self.client.get('/studybuddy/' + self.test_email,)
        self.assertEqual(response.status_code, 301)

    def test_view_url_exists_at_desired_location(self):
        """
        url is valid to view the homepage

        Source for "follow=True" - https://stackoverflow.com/questions/21215035/django-test-always-returning-301
        """
        response = self.client.get('/studybuddy/' + self.test_email, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """
        homepage view is accessible through its name
        301 because after login homepage is redirected
        """
        response = self.client.get(reverse('studybuddy:index', args = (self.test_email,)))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        homepage view uses the correct template
        """
        response = self.client.get(reverse('studybuddy:index', args = (self.test_email, )))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

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

    def test_view_url_exists_at_desired_location(self):
        """
        url is valid to view all the departments
        """
        response = self.client.get('/studybuddy/' + self.test_dept, follow=True)
        self.assertEqual(response.status_code, 200)

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

    def test_no_courses(self):
        """
        If no courses exist, an appropriate message is displayed.
        **this most likely will occur if the department id is incorrect
        """
        response = self.client.get(reverse('studybuddy:department', args = (self.test_email, self.test_dept,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No classes are available in " + self.test_dept.upper() + " or " +
                            self.test_dept.upper() + " does not exist.")

    def test_passing_string_as_dept(self):
        """
        when url received is not a desired format throw a 404 error?
        when url received is not a number still displays desired error message
        """
        pass

    # OH: mocking Department
    # def test_passing_a_valid_department_courses_are_displayed(self):
    #     """
    #     Add test_dept to Departments Model
    #     Add courses to Course model
    #
    #     Test url that test courses show up
    #     """
    #     # given
    #     test_catalog_number = 1234
    #     test_instructor = 'testInstructor'
    #     test_section = 000
    #     test_course_number = 12345
    #     Departments.objects.create(dept=self.test_dept)
    #
    #     Course.objects.create(subject=self.test_dept,
    #                           catalog_number=test_catalog_number,
    #                           instructor=test_instructor,
    #                           section=test_section,
    #                           course_number=test_course_number)
    #
    #     print(Departments.objects.all())
    #
    #     # when
    #     response = self.client.get(reverse('studybuddy:department', args=(self.test_email, self.test_dept,)))
    #     print(response.content)
    #
    #     # then
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, Course.objects.get(subject=self.test_dept))
    #

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

        # mock user login
        self.test_user = get_user_model().objects.create_user(self.test_username, self.test_email, self.test_password)
        self.client.login(username=self.test_username, password=self.test_password)

    # def test_view_url_exists_at_desired_location(self):
    #     """
    #     url is valid to view all the departments
    #     """
    #     response = self.client.get(('/studybuddy/', self.test_subject, '/', self.test_course_number), follow=True)
    #     self.assertEqual(response.status_code, 200)

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

    def test_view_nofeed(self):
        """
        when there are no study buddy posts for the course, the feed displays appropriate message
        """
        response = self.client.get(
            reverse('studybuddy:coursefeed', args=(self.test_email, self.test_subject, self.test_course_number)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are currently no posts made for this class")

    # Source: https://stackoverflow.com/questions/45512749/how-to-mock-a-django-model-object-along-with-its-methods

    # OH: mocking course and feed
    # @mock.patch('studybuddy.models.Course.objects', 'studybuddy.models.Post.objects')
    # def test_views_displays_feed(self, mock_course, mock_post):
    #     """
    #     when there are study buddy post for the course, the feed displays
    #     """
    #
    #     # given
    #     test_topic = "test_topic"
    #     test_description = "test_description"
    #
    #     Departments.objects.create(dept=self.test_subject.upper())
    #
    #     # test_course = Course.objects.create(subject=self.test_subject.upper(),
    #     #                       catalog_number=self.test_catalog_number,
    #     #                       instructor=self.test_instructor,
    #     #                       section=self.test_section,
    #     #                       course_number=self.test_course_number)
    #
    #     test_user = User.objects.create(email=self.test_email)
    #
    #     # test_post = Post.objects.create(course=test_course,
    #     #                     user=test_user,
    #     #                     author=self.test_username,
    #     #                     topic=test_topic,
    #     #                     startDate=timezone.now(),
    #     #                     endDate=timezone.now() + datetime.timedelta(days=7),
    #     #                     description=test_description)
    #
    #     mock_course.filter.exists.return_value = True
    #     mock_course.filter.return_value = mock_course #test_course
    #     mock_post.filter.return_value = mock_post #test_post
    #
    #     # when
    #     response = self.client.get(
    #         reverse('studybuddy:coursefeed', args=(self.test_email, self.test_subject, self.test_course_number)))
    #
    #     # then
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, test_topic)
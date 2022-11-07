# Source: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
from django.urls import reverse
from django.test import TestCase

class LoginViewTest(TestCase):
    """
    When the user is not logged in, all of the pages except index and all departments,
    because they are classes will use the index.html template
    """
    def setUp(self):
        self.test_email = 'test@email.com'
        self.test_dept = 'testDept'
        self.test_course_number = 12345

    def test_homepage(self):
        response = self.client.get(reverse('studybuddy:index', args = (self.test_email,)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login with Google")
        self.assertTemplateUsed(response, 'index.html')

    def test_account(self):
        response = self.client.get(reverse('studybuddy:account', args = (self.test_email,)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login with Google")
        self.assertTemplateUsed(response, 'index.html')

    def test_addAccount(self):
        response = self.client.get(reverse('studybuddy:addAccount', args = (self.test_email,)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login With Google")
        self.assertTemplateUsed(response, 'index.html')

    def test_editAccount(self):
        response = self.client.get(reverse('studybuddy:editAccount', args = (self.test_email,)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login With Google")
        self.assertTemplateUsed(response, 'index.html')

    def test_updateAccount(self):
        response = self.client.get(reverse('studybuddy:updateAccount', args = (self.test_email,)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login With Google")
        self.assertTemplateUsed(response, 'index.html')

    def test_alldepartments(self):
        response = self.client.get(reverse('studybuddy:alldepartments', args = (self.test_email,)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login With Google")
        self.assertTemplateUsed(response, 'alldepartments.html')

    def test_department(self):
        response = self.client.get(reverse('studybuddy:department', args = (self.test_email, self.test_dept)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login With Google")
        self.assertTemplateUsed(response, 'index.html')

    def test_coursefeed(self):
        response = self.client.get(reverse('studybuddy:coursefeed', args = (self.test_email,
                                                                            self.test_dept,
                                                                            self.test_course_number)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login With Google")
        self.assertTemplateUsed(response, 'index.html')

    def test_makepost(self):
        response = self.client.get(reverse('studybuddy:makepost', args = (self.test_email,
                                                                          self.test_dept,
                                                                          self.test_course_number)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login With Google")
        self.assertTemplateUsed(response, 'index.html')

    def test_submitpost(self):
        response = self.client.get(reverse('studybuddy:submitpost', args=(self.test_email,
                                                                          self.test_dept,
                                                                          self.test_course_number)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login With Google")
        self.assertTemplateUsed(response, 'index.html')

    def test_viewposts(self):
        response = self.client.get(reverse('studybuddy:viewposts'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Login With Google")
        self.assertTemplateUsed(response, 'index.html')
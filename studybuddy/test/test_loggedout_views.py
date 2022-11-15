from django.urls import reverse
from django.test import TestCase

class LoginViewTest(TestCase):
    """
    When the user is not logged in, all of the pages except index and all departments,
    because they are classes will use the index.html template
    """
    def setUp(self):
        self.test_dept = 'testDept'
        self.test_course_number = 12345
        self.test_requestee_email = 'test_requestee@email.com'
        self.test_room_number = 1

    def test_homepage(self):
        response = self.client.get(reverse('studybuddy:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    # def test_send_friend_request(self):
    #     response = self.client.get(reverse('studybuddy:send friend request', args=(self.test_requestee_email,)))
    #     self.assertEqual(response.status_code, 302) # 200)
    #     self.assertContains(response, "Do you want to study with me?")
    #     self.assertTemplateUsed(response, 'index.html')
    #
    # def test_accept_friend_request(self):
    #     response = self.client.get(reverse('studybuddy:accept friend request', args=(self.test_requestee_email,)))
    #     self.assertEqual(response.status_code, 302) #200)
    #     self.assertContains(response, "Do you want to study with me?")
    #     self.assertTemplateUsed(response, 'index.html')

    def test_account(self):
        response = self.client.get(reverse('studybuddy:account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    def test_addAccount(self):
        response = self.client.get(reverse('studybuddy:addAccount'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    def test_editAccount(self):
        response = self.client.get(reverse('studybuddy:editAccount'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    def test_updateAccount(self):
        response = self.client.get(reverse('studybuddy:updateAccount'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    def test_alldepartments(self):
        response = self.client.get(reverse('studybuddy:alldepartments'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    def test_department(self):
        response = self.client.get(reverse('studybuddy:department', args = (self.test_dept,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    def test_coursefeed(self):
        response = self.client.get(reverse('studybuddy:coursefeed', args = (self.test_dept,
                                                                            self.test_course_number)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    def test_makepost(self):
        response = self.client.get(reverse('studybuddy:makepost', args = (self.test_dept,
                                                                          self.test_course_number)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    def test_viewposts(self):
        response = self.client.get(reverse('studybuddy:viewposts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    def test_schedule(self):
        response = self.client.get(reverse('studybuddy:schedule', args=(self.test_room_number,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')

    def test_upcoming_sessions(self):
        response = self.client.get(reverse('studybuddy:upcomingSessions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Do you want to study with me?")
        self.assertTemplateUsed(response, 'index.html')
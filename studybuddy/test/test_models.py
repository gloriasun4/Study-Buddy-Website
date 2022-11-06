from django.test import TestCase
from studybuddy.models import User, Course
from django.urls import reverse

class CourseTest(TestCase):
    def setUp(self):
        self.test_subject = 'testDept'
        self.test_catalog_number = '1234'
        self.test_instructor = 'testInstructor'
        self.test_section = '000'
        self.test_course_number = '12345'

        Course.objects.create(subject=self.test_subject,
                               catalog_number=self.test_catalog_number,
                               instructor=self.test_instructor,
                               section=self.test_section,
                               course_number=self.test_course_number)

    def test_course_str(self):
        """
        Check the _str_ methods displays correctly when a course has all valid value
        """
        expectedStr = self.test_subject + self.test_catalog_number + ' \n ' + \
                      'Instructor: ' + self.test_instructor + ' \n ' +\
                      '(Section: ' + self.test_section + ')'
        self.assertEqual(Course.objects.get(course_number = self.test_course_number).__str__(), expectedStr)

    def test_no_instructor_available(self):
        """
        Check the _str_ methods displays correctly with instructor is '-'
        """
        test_dept = Course(subject =self.test_subject,
                          catalog_number = self.test_catalog_number,
                          instructor = '-',
                          section = self.test_section,
                          course_number = self.test_course_number)
        expectedStr = self.test_subject + self.test_catalog_number + ' \n ' + \
                      'Instructor: Not available' + ' \n ' +\
                      '(Section: ' + self.test_section + ')'
        self.assertEqual(test_dept.__str__(), expectedStr)

    def test_subject_label(self):
        test_course = Course.objects.get(id=1)
        expected_label = test_course._meta.get_field('subject').verbose_name
        self.assertEqual(expected_label, 'subject')
    # test for a class being added successfully to the model
    # create a mock department and assert true/false


class UserTest(TestCase):
    def test_default(self):
        account = User(email="abc@gmail.com")
        self.assertEqual(account.email, "abc@gmail.com")
        self.assertEqual(account.firstName, "")
        self.assertEqual(account.lastName, "")
        self.assertEqual(account.zoomLink, "")
        self.assertEqual(account.blurb, "")

    def test_update(self):
        account = User(email="abc2@gmail.com")
        account.firstName="abc"
        account.blurb="hi my name is abc"
        self.assertEqual(account.email, "abc2@gmail.com")
        self.assertEqual(account.firstName, "abc")
        self.assertEqual(account.lastName, "")
        self.assertEqual(account.zoomLink, "")
        self.assertEqual(account.blurb, "hi my name is abc")

class EnrollTest(TestCase):
    def add_class(self):
        account = User(email="abc3@gmail.com", firstName="abc", lastName="def")
        test_course = Course.objects.get(id=1)
        enroll= EnrolledClass(course=test_course, student=account)
        enrolled_course = account.enrolledclass_set.all()
        num_enrolled_course = account.enrolledclass_set.count()
        self.assertTrue(EnrolledClass.objects.filter(course=test_course, student=account).exists())
        self.assertEqual(num_enrolled_course, 1)



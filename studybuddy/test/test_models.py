from django.urls import reverse
from django.test import TestCase
from studybuddy.models import User, Course, Post

class CourseTest(TestCase):
    def setUp(self):
        self.test_subject = 'testDept'
        self.test_catalog_number = '1234'
        self.test_instructor = 'testInstructor'
        self.test_section = '000'
        self.test_course_number = '12345'
        self.test_description = 'testDescription'

        Course.objects.create(subject=self.test_subject,
                               catalog_number=self.test_catalog_number,
                               instructor=self.test_instructor,
                               section=self.test_section,
                               course_number=self.test_course_number,
                               description=self.test_description)

    def test_course_str(self):
        """
        Check the _str_ methods displays correctly when a course has all valid value
        """
        # given
        expectedStr = self.test_subject + self.test_catalog_number + ": " + self.test_description + ' \n ' + \
                      'Instructor: ' + self.test_instructor + ' \n ' +\
                      '(Section: ' + self.test_section + ')'

        # then
        self.assertEqual(Course.objects.get(course_number = self.test_course_number).__str__(), expectedStr)

    def test_no_instructor_available(self):
        """
        Check the _str_ methods displays correctly with instructor is '-'
        """
        test_dept = Course(subject =self.test_subject,
                          catalog_number = self.test_catalog_number,
                          instructor = '-',
                          section = self.test_section,
                          course_number = self.test_course_number,
                          description = self.test_description)
        expectedStr = self.test_subject + self.test_catalog_number + ": " + self.test_description + ' \n ' + \
                      'Instructor: Not available' + ' \n ' +\
                      '(Section: ' + self.test_section + ')'
        self.assertEqual(test_dept.__str__(), expectedStr)

    def test_subject_label(self):
        test_course = Course.objects.get(id=1)
        expected_label = test_course._meta.get_field('subject').verbose_name
        self.assertEqual(expected_label, 'subject')

    # test for a class being added successfully to the model
    # create a mock department and assert true/false

class PostTest(TestCase):
    def setUp(self):
        self.test_subject = 'testDept'
        self.test_catalog_number = '1234'
        self.test_instructor = 'testInstructor'
        self.test_section = '000'
        self.test_course_number = '12345'
        self.test_description = 'testDescription'

        test_course = Course.objects.create(subject=self.test_subject,
                              catalog_number=self.test_catalog_number,
                              instructor=self.test_instructor,
                              section=self.test_section,
                              course_number=self.test_course_number,
                              description=self.test_description)

        self.test_email = 'test@email.com'

        test_user = User.objects.create(email=self.test_email)

        self.test_author = 'testAuthor'
        self.test_topic = 'test_topic'
        self.start_date = '1111-01-01'
        self.end_date = '1111-01-02'

        Post.objects.create(course=test_course,
                            user=test_user,
                            author=self.test_author,
                            topic=self.test_topic,
                            startDate=self.start_date,
                            endDate=self.end_date)

    def test_post_str(self):
        """
        Check _str_ methods returns correctly for Posts
        """
        # given
        expectedStr = self.test_topic + '\n' + \
                      'Author: ' + self.test_author + '\n' + \
                      'Time Frame: ' + self.start_date + ' to ' + self.end_date + '\n'

        # when
        actualStr = Post.objects.get(author = self.test_author).__str__()

        # then
        self.assertEqual(actualStr, expectedStr)
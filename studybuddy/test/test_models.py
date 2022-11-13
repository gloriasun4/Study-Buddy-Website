from django.test import TestCase
from studybuddy.models import User, Course, Post, StudySession


class CourseTest(TestCase):
    def setUp(self):
        self.test_subject = 'testDept'
        self.test_catalog_number = '1234'
        self.test_instructor = 'testInstructor'
        self.test_section = '000'
        self.test_course_number = '12345'
        self.test_description = 'testDescription'

        self.test_course = Course.objects.create(subject=self.test_subject,
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
                      'Instructor: ' + self.test_instructor + ' \n ' + \
                      '(Section: ' + self.test_section + ')'

        # then
        self.assertEqual(self.test_course.__str__(), expectedStr)

    def test_no_instructor_available(self):
        """
        Check the _str_ methods displays correctly with instructor is '-'
        """
        # given
        test_course = Course(subject=self.test_subject,
                           catalog_number=self.test_catalog_number,
                           instructor='-',
                           section=self.test_section,
                           course_number=self.test_course_number,
                           description=self.test_description)

        # then
        expectedStr = self.test_subject + self.test_catalog_number + ": " + self.test_description + ' \n ' + \
                      'Instructor: Not available' + ' \n ' + \
                      '(Section: ' + self.test_section + ')'
        self.assertEqual(test_course.__str__(), expectedStr)

    def test_subject_label(self):
        expected_label = self.test_course._meta.get_field('subject').verbose_name
        self.assertEqual(expected_label, 'subject')

    # test for a class being added successfully to the model
    # create a mock department and assert true/false


class UserTest(TestCase):
    def test_default(self):
        account = User(email="abc@gmail.com")
        self.assertEqual(account.email, "abc@gmail.com")
        self.assertEqual(account.name, "")
        self.assertEqual(account.zoomLink, "")
        self.assertEqual(account.blurb, "")

    def test_update(self):
        account = User(email="abc2@gmail.com")
        account.name = "abc"
        account.blurb = "hi my name is abc"
        self.assertEqual(account.email, "abc2@gmail.com")
        self.assertEqual(account.name, "abc")
        self.assertEqual(account.zoomLink, "")
        self.assertEqual(account.blurb, "hi my name is abc")


class EnrollTest(TestCase):
    def add_class(self):
        account = User(email="abc3@gmail.com", firstName="abc", lastName="def")
        test_course = Course.objects.get(id=1)
        enroll = EnrolledClass(course=test_course, student=account)
        enrolled_course = account.enrolledclass_set.all()
        num_enrolled_course = account.enrolledclass_set.count()
        self.assertTrue(EnrolledClass.objects.filter(course=test_course, student=account).exists())
        self.assertEqual(num_enrolled_course, 1)


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
        self.start_date = '01-01-2022'
        self.end_date = '01-02-2022'

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
        actualStr = Post.objects.get(author=self.test_author).__str__()

        # then
        self.assertEqual(actualStr, expectedStr)


class StudySessionTest(TestCase):
    def setUp(self):
        self.test_name = 'testName'
        self.test_date = '01-01-2022'
        self.test_start = '11:22'
        self.test_end = '12:22'
        self.test_accepted = '?'

        StudySession.objects.create(name=self.test_name,
                                    date=self.test_date,
                                    start=self.test_start,
                                    end=self.test_end)

    def test_study_session_str(self):
        """
        check __str__ methods return correctly for StudySession
        """
        # given
        expected_str = "Study session for: " + self.test_name + '\n' \
                       + "Scheduled on: " + self.test_date + '\n' \
                       + "Time Frame: " + self.test_start + ' to ' + self.test_end

        # when
        actual_str = StudySession.objects.get(name=self.test_name).__str__()

        # then
        self.assertEqual(actual_str, expected_str)

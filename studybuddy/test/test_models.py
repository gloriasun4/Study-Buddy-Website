# from django.test import TestCase
# from studybuddy.models import User, Course
# from django.urls import reverse
#
# # Create your test here.
# class ModelTesting(TestCase):
#     def test_model(self):
#         self.user = User.objects.create(username='jacqueline-chao', password='123')
#         self.assertTrue(isinstance(self.user, User))
#
# class CourseTest(TestCase):
#     def setUp(self):
#         self.test_subject = 'testDept'
#         self.test_catalog_number = '1234'
#         self.test_instructor = 'testInstructor'
#         self.test_section = '000'
#         self.test_course_number = '12345'
#
#         Course.objects.create(subject=self.test_subject,
#                                catalog_number=self.test_catalog_number,
#                                instructor=self.test_instructor,
#                                section=self.test_section,
#                                course_number=self.test_course_number)
#
#     def test_course_str(self):
#         """
#         Check the _str_ methods displays correctly when a course has all valid value
#         """
#         expectedStr = self.test_subject + self.test_catalog_number + ' \n ' + \
#                       'Instructor: ' + self.test_instructor + ' \n ' +\
#                       '(Section: ' + self.test_section + ')'
#         self.assertEqual(Course.objects.get(course_number = self.test_course_number).__str__(), expectedStr)
#
#     def test_no_instructor_available(self):
#         """
#         Check the _str_ methods displays correctly with instructor is '-'
#         """
#         test_dept = Course(subject =self.test_subject,
#                           catalog_number = self.test_catalog_number,
#                           instructor = '-',
#                           section = self.test_section,
#                           course_number = self.test_course_number)
#         expectedStr = self.test_subject + self.test_catalog_number + ' \n ' + \
#                       'Instructor: Not available' + ' \n ' +\
#                       '(Section: ' + self.test_section + ')'
#         self.assertEqual(test_dept.__str__(), expectedStr)
#
#     def test_subject_label(self):
#         test_course = Course.objects.get(id=1)
#         expected_label = test_course._meta.get_field('subject').verbose_name
#         self.assertEqual(expected_label, 'subject')
#     # test for a class being added successfully to the model
#     # create a mock department and assert true/false
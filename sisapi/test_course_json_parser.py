import json

from django.test import TestCase

from .models import *
from .course_json_parser import CourseJsonParser


def cs1110_001_json_string():
    return """
    {
        "index": 2,
        "crse_id": "006846",
        "crse_offer_nbr": 1,
        "strm": "1228",
        "session_code": "SRT",
        "session_descr": "Short Add",
        "class_section": "001",
        "location": "MAIN",
        "location_descr": "On Grounds",
        "start_dt": "08/23/2022",
        "end_dt": "12/06/2022",
        "class_stat": "A",
        "campus": "MAIN",
        "campus_descr": "Main Campus",
        "class_nbr": 16003,
        "acad_career": "UGRD",
        "acad_career_descr": "Undergraduate",
        "component": "LEC",
        "subject": "CS",
        "subject_descr": "Computer Science",
        "catalog_nbr": "1110",
        "class_type": "E",
        "schedule_print": "Y",
        "acad_group": "ENGR",
        "instruction_mode": "P",
        "instruction_mode_descr": "In Person",
        "acad_org": "CS",
        "wait_tot": 0,
        "wait_cap": 199,
        "class_capacity": 275,
        "enrollment_total": 274,
        "enrollment_available": 1,
        "descr": "Introduction to Programming",
        "rqmnt_designtn": "",
        "units": "3",
        "combined_section": "N",
        "enrl_stat": "O",
        "enrl_stat_descr": "Open",
        "topic": "",
        "instructors": [
          {
            "name": "Raymond Pettit",
            "email": "rp6zr@virginia.edu"
          }
        ],
        "section_type": "Lecture",
        "meetings": [
          {
            "days": "MoWeFr",
            "start_time": "14.00.00.000000-05:00",
            "end_time": "14.50.00.000000-05:00",
            "start_dt": "08/23/2022",
            "end_dt": "12/06/2022",
            "bldg_cd": "WNR",
            "bldg_has_coordinates": false,
            "facility_descr": "John W. Warner Hall 209",
            "room": "209",
            "facility_id": "WNR 209",
            "instructor": "Raymond Pettit"
          }
        ],
        "crse_attr": "NCLC",
        "crse_attr_value": "NCLC-NOCOST",
        "reserve_caps": []
    }"""


def cs3240_002_json_string():
    return """
    {
    "index": 48,
    "crse_id": "006903",
    "crse_offer_nbr": 1,
    "strm": "1228",
    "session_code": "SRT",
    "session_descr": "Short Add",
    "class_section": "001",
    "location": "MAIN",
    "location_descr": "On Grounds",
    "start_dt": "08/23/2022",
    "end_dt": "12/06/2022",
    "class_stat": "A",
    "campus": "MAIN",
    "campus_descr": "Main Campus",
    "class_nbr": 15991,
    "acad_career": "UGRD",
    "acad_career_descr": "Undergraduate",
    "component": "LEC",
    "subject": "CS",
    "subject_descr": "Computer Science",
    "catalog_nbr": "3240",
    "class_type": "E",
    "schedule_print": "Y",
    "acad_group": "ENGR",
    "instruction_mode": "P",
    "instruction_mode_descr": "In Person",
    "acad_org": "CS",
    "wait_tot": 0,
    "wait_cap": 199,
    "class_capacity": 135,
    "enrollment_total": 134,
    "enrollment_available": 1,
    "descr": "Advanced Software Development Techniques",
    "rqmnt_designtn": "",
    "units": "3",
    "combined_section": "N",
    "enrl_stat": "C",
    "enrl_stat_descr": "Closed",
    "topic": "",
    "instructors": [
      {
        "name": "Paul McBurney",
        "email": "pm8fc@virginia.edu"
      },
      {
        "name": "Mark Sherriff",
        "email": "mss2x@virginia.edu"
      }
    ],
    "section_type": "Lecture",
    "meetings": [
      {
        "days": "TuTh",
        "start_time": "15.30.00.000000-05:00",
        "end_time": "16.45.00.000000-05:00",
        "start_dt": "08/23/2022",
        "end_dt": "12/06/2022",
        "bldg_cd": "RICE",
        "bldg_has_coordinates": true,
        "facility_descr": "Rice Hall 130",
        "room": "130",
        "facility_id": "RICE 130",
        "instructor": "Paul McBurney"
      }
    ],
    "crse_attr": "",
    "crse_attr_value": "",
    "reserve_caps": []
  }
    """


def cs2130_001_json_string():
    return """
    {
    "index": 31,
    "crse_id": "046226",
    "crse_offer_nbr": 1,
    "strm": "1228",
    "session_code": "SRT",
    "session_descr": "Short Add",
    "class_section": "001",
    "location": "MAIN",
    "location_descr": "On Grounds",
    "start_dt": "08/23/2022",
    "end_dt": "12/06/2022",
    "class_stat": "A",
    "campus": "MAIN",
    "campus_descr": "Main Campus",
    "class_nbr": 19682,
    "acad_career": "UGRD",
    "acad_career_descr": "Undergraduate",
    "component": "LEC",
    "subject": "CS",
    "subject_descr": "Computer Science",
    "catalog_nbr": "2130",
    "class_type": "E",
    "schedule_print": "Y",
    "acad_group": "ENGR",
    "instruction_mode": "P",
    "instruction_mode_descr": "In Person",
    "acad_org": "CS",
    "wait_tot": 0,
    "wait_cap": 199,
    "class_capacity": 315,
    "enrollment_total": 306,
    "enrollment_available": 9,
    "descr": "Computer Systems and Organization 1",
    "rqmnt_designtn": "",
    "units": "4",
    "combined_section": "N",
    "enrl_stat": "O",
    "enrl_stat_descr": "Open",
    "topic": "",
    "instructors": [
      {
        "name": "Robbie Hott",
        "email": "jh2jf@virginia.edu"
      }
    ],
    "section_type": "Lecture",
    "meetings": [
      {
        "days": "WeFr",
        "start_time": "14.00.00.000000-05:00",
        "end_time": "14.50.00.000000-05:00",
        "start_dt": "08/23/2022",
        "end_dt": "12/06/2022",
        "bldg_cd": "CHM",
        "bldg_has_coordinates": true,
        "facility_descr": "Chemistry Bldg 402",
        "room": "402",
        "facility_id": "CHM 402",
        "instructor": "Robbie Hott"
      },
      {
        "days": "Mo",
        "start_time": "14.00.00.000000-05:00",
        "end_time": "14.50.00.000000-05:00",
        "start_dt": "08/23/2022",
        "end_dt": "12/06/2022",
        "bldg_cd": "GIL",
        "bldg_has_coordinates": true,
        "facility_descr": "Gilmer Hall 301",
        "room": "301",
        "facility_id": "GIL 301",
        "instructor": "Robbie Hott"
      }
    ],
    "crse_attr": "NCLC",
    "crse_attr_value": "NCLC-NOCOST",
    "reserve_caps": []
  }
    """


class CourseJsonParserTest(TestCase):
    def setUp(self):
        Instructor.objects.create(name="Raymond Pettit", email="rp6zr@virginia.edu")

    def test_get_instructor_one_instructor(self):
        cs1110 = json.loads(cs1110_001_json_string())
        cjp = CourseJsonParser(cs1110)
        ray = cjp.get_instructor()
        self.assertEqual(ray.name, "Raymond Pettit")
        self.assertEqual(ray.email, "rp6zr@virginia.edu")


    def test_get_instructor_two_instructors(self):
        cs3240 = json.loads(cs3240_002_json_string())
        cjp = CourseJsonParser(cs3240)
        baldy = cjp.get_instructor()
        self.assertEqual(baldy.name, "Paul McBurney")  # Not Will
        self.assertEqual(baldy.email, "pm8fc@virginia.edu")

    def test_get_section_cs1110(self):
        cs1110 = json.loads(cs1110_001_json_string())
        cjp = CourseJsonParser(cs1110)
        course1110 = cjp.get_section()
        self.assertEqual(course1110.course_number, 16003)
        self.assertEqual(course1110.semester_code, 1228)
        self.assertEqual(course1110.course_section, "001")
        self.assertEqual(course1110.subject, "CS")
        self.assertEqual(course1110.catalog_number, "1111")
        self.assertEqual(course1110.description, "Introduction to Programming")
        self.assertEqual(course1110.units, "3")
        self.assertEqual(course1110.component, "LEC")
        self.assertEqual(course1110.class_capacity, 275)
        self.assertEqual(course1110.wait_list, 0)
        self.assertEqual(course1110.wait_cap, 199)
        self.assertEqual(course1110.enrollment_total, 274)
        self.assertEqual(course1110.enrollment_available, 1)
        self.assertEqual(course1110.topic, "")

    def test_get_meet_cs1110(self):
        cs1110 = json.loads(cs1110_001_json_string())
        cjp = CourseJsonParser(cs1110)
        course1110 = cjp.get_meetings()
        meeting = course1110[0]
        self.assertEqual(meeting.days, "MoWeFr")
        self.assertEqual(meeting.start_time, "14.00.00.000000-05:00")
        self.assertEqual(meeting.end_time, "14.50.00.000000-05:00")
        self.assertEqual(meeting.facility_description, "John W. Warner Hall 209")

    def test_get_meet_different_meetings(self):
        cs2130 = json.loads(cs2130_001_json_string())
        cjp = CourseJsonParser(cs2130)
        course1110 = cjp.get_meetings()
        meeting0 = course1110[0]
        self.assertEqual(meeting0.days, "WeFr")
        self.assertEqual(meeting0.start_time, "14.00.00.000000-05:00")
        self.assertEqual(meeting0.end_time, "14.50.00.000000-05:00")
        self.assertEqual(meeting0.facility_description, "Chemistry Bldg 402")
        meeting1 = course1110[1]
        self.assertEqual(meeting1.days, "Mo")
        self.assertEqual(meeting1.start_time, "14.00.00.000000-05:00")
        self.assertEqual(meeting1.end_time, "14.50.00.000000-05:00")
        self.assertEqual(meeting1.facility_description, "Gilmer Hall 301")







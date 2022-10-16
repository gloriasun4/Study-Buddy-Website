from .models import *


class CourseJsonParser:
    def __init__(self, json_object):
        self.json_object = json_object

    def get_instructor(self):
        instructor_array = self.json_object["instructors"]
        first_instructor_json = instructor_array[0]
        name = first_instructor_json["name"]
        email = first_instructor_json["email"]
        if not Instructor.objects.filter(email=email).exists():
            Instructor.objects.create(name=name, email=email)
        return Instructor.objects.get(email=email)

    def get_section(self):
        instructor = self.get_instructor()
        if not Instructor.objects.filter(email=instructor.email).exists():
            raise RuntimeError("Instructor doesn't exist and hasn't been created")
        section = Section(instructor=instructor,
                          course_number=self.json_object["class_nbr"],
                          semester_code=int(self.json_object["strm"]),
                          course_section=self.json_object["class_section"],
                          subject=self.json_object["subject"],
                          catalog_number=self.json_object["catalog_nbr"],
                          description=self.json_object["descr"],
                          units=self.json_object["units"],
                          component=self.json_object["component"],
                          class_capacity=self.json_object["class_capacity"],
                          wait_list=self.json_object["wait_tot"],
                          wait_cap=self.json_object["wait_cap"],
                          enrollment_total=self.json_object["enrollment_total"],
                          enrollment_available=self.json_object["enrollment_available"],
                          topic=self.json_object["topic"]
                          )
        if not Section.objects.filter(course_number=section.course_number).exists():
            section.save()
        return Section.objects.get(course_number=section.course_number)

    def get_meetings(self):
        section = self.get_section()
        if not Section.objects.filter(course_number=section.course_number).exists():
            raise RuntimeError("Section doesn't exist and hasn't been created")
        if Meeting.objects.filter(section=section).exists():
            return Meeting.objects.filter(section=section)
        meetings = []
        for meeting in self.json_object["meetings"]:
            new_meeting = Meeting(section=section,
                                  days=meeting["days"],
                                  start_time=meeting["start_time"],
                                  end_time=meeting["end_time"],
                                  facility_description=meeting["facility_descr"])
            meetings.append(new_meeting)
        for meeting in meetings:
            meeting.save()
        return meetings

    def load_all(self):
        self.get_meetings()

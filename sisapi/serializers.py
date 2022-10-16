# Serializers to support JSON parsing

from rest_framework import serializers
from .models import Section, Instructor, Meeting


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['name', 'email']

class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = ['days', 'start_time', 'end_time', 'facility_description']


class SectionSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer()
    meetings = MeetingSerializer(many=True)

    class Meta:
        model = Section
        fields = ['instructor', 'course_number', 'semester_code', 'course_section', 'subject', 'catalog_number', 'description', 'units', 'component', 'class_capacity', 'wait_list', 'wait_cap', 'enrollment_total', 'enrollment_available', 'topic', 'meetings']

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ['subject']


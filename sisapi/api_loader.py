import json
import os
from listapi.course_json_parser import CourseJsonParser


def get_all_json_files():
    json_files = []
    for root, dirs, files in os.walk('JSON'):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    for each in json_files:
        print(each)
        load_json_file(each)


def load_json_file(filename):
    print("Opening:",filename)
    json_file = open(filename, 'r')
    json_string = json_file.read()
    load_json_string(json_string)


def load_json_string(json_string):
    json_array = json.loads(json_string)
    load_json_array(json_array)


def load_json_array(json_array):
    for json_object in json_array:
        load_database_from_json_object(json_object)


def load_database_from_json_object(json_object):
    cpj = CourseJsonParser(json_object)
    cpj.load_all()

from flask import (
    Blueprint, render_template
)
import flaskr.db as db



def parse_search(search_string):
    string_list = search_string.split()
    dept = None
    code = None
    school = None
    schools_in_db = db.get_schools()

    for string in string_list:
        if string[0].isnumeric():
            code = string
        elif string in schools_in_db:
            school = string
        else:
            dept = string
    return [dept, code, school]


def search(search_list):
    dept = search_list[0]
    code = search_list[1]
    school = search_list[2]
    exams = db.get_exam_db(dept=dept, course_number=code, school_name=school)
    return exams

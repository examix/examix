from flask import (
    Blueprint, render_template
)
import json
from flaskr.exam import Exam, Page, Question
import flaskr.db

bp = Blueprint('performatted_parser', __name__)

@bp.route('/populate')
def json_to_db():
    ex = read_json('flaskr/sample_data/CPSC101Q1.json')
    flaskr.db.insert_full_exam(ex, ex.department, ex.course_code) 
    return 'success'

def read_json(fname) -> Exam:
    with open(fname) as fp:
        contents = json.load(fp)

    exam_pages = contents.get('num_pages')
    difficulty = contents.get('difficulty')
    prof = contents.get('prof')
    pdf_name = contents.get('pdf_name')
    duration = contents.get('duration')
    date = contents.get('date')
    exam_type = contents.get('exam_type')
    num_questions = contents.get('num_questions')
    num_points = contents.get('num_points')
    school = contents.get('school')
    department = contents.get('department')
    course_code = contents.get('course_code')

    pages = []
    for page in contents.get('pages'):
        page_num = page.get('page_num')
        width = page.get('width')
        height = page.get('height')

        questions = []
        for question in page.get('questions'):
            text = question.get('question_text')
            q_difficulty = question.get('difficulty')
            q_page_num = question.get('page_num')
            verticies = question.get('verticies')
            question_type = question.get('question_type')
            q_num_points = question.get('num_points')
            exam_image = question.get('exam_image')
            q_duration = question.get('duration')
            answer = None

            questions.append(Question(text, q_difficulty, q_page_num, verticies, question_type, q_num_points, exam_image, q_duration, answer))

        pages.append(Page(page_num, width, height, questions))
    return Exam(exam_pages, difficulty, prof, pdf_name, duration, date, exam_type, num_questions, num_points, pages, school, department, course_code)

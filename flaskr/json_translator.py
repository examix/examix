from flask import (
    Blueprint, render_template
)
import json
from flaskr.exam import Exam, Page, Question
import flaskr.db as db
import flaskr.json_parser as json_parser
import flaskr.remix_functions as rf
import flaskr.sample_data.preformatted_parser as pf
import base64, io
import math

bp = Blueprint('json_translator', __name__)

@bp.route('/test', methods=['GET', 'POST'])
def test():
    print('hit')

@bp.route('/request')
def index():
    db.insert_default_school('uvic', 'victoria', 'canada')
    db.insert_alternate_school('uvic', 'university of victoria')

    db.insert_default_school('ubc', 'vancouver', 'canada')
    db.insert_alternate_school('ubc', 'university of british columbia')

    db.insert_course_full_db('CPSC', '101', 'Connecting with Computer Science', 
                             'Learn Computer Science', 'ubc')

    pf.json_to_db('flaskr/sample_data/CPSC101Q1.json')
    pf.json_to_db('flaskr/sample_data/CPSC101Q3.json')
    '''
    ext_to_parse = open("file.json", "r")
    text = json.loads(text_to_parse.read())

    exam_dur = json_parser.search_duration(text)
    exam_points = json_parser.search_points(json_parser.get_intro_text(text['text']))
    test = parse_pages(text, exam_points, exam_dur)
    exam = create_exam(test, exam_points, exam_dur)

    db.insert_full_exam(exam)
    
    exam = db.get_exam_db(school_name="ubc") # gets random exam from db

    return render_template('pages/testing_parser.html', test=test, exam=exam)
    '''
    return "success"


# returns a list of pages for a specific exam
def parse_pages(text, exam_points, exam_dur):
    pages = text['pages']
    pages_list = []
    for page_idx, page in enumerate(pages):
        page_num = page['pageNumber']
        width = page['dimension']['width']
        height = page['dimension']['height']
        cur_page = Page(page_num, width, height)
        img = base64.decodebytes(bytes(page['image']['content'], 'utf-8'))


        # get questions for this page
        cur_page.questions = parse_questions(text, page_idx, page_num, img, exam_points, exam_dur)
        pages_list.append(cur_page)
    return pages_list


def parse_questions(text, page_idx, page_num, img, exam_points, exam_dur):
    question_blocks = json_parser.get_question_blocks(text, page_idx)
    cur_questions = []
    for question_block in question_blocks:
        question_text = json_parser.get_question_text(text, question_block)
        difficulty = None
        page_num = page_num
        vertices = json_parser.get_question_bounds(question_block)
        question_type = None
        num_points = json_parser.search_points(question_text)

        with io.BytesIO(img) as imgfp:
            exam_image = json_parser.extract_question_image(imgfp, vertices)

        duration = round((num_points / exam_points) * exam_dur / 60)
        cur_question = Question(question_text, difficulty, page_num, vertices,
                                question_type, num_points, exam_image, duration)
        cur_questions.append(cur_question)
    return cur_questions


def create_exam(pages, exam_points, exam_dur):
    num_pages = len(pages)
    difficulty = 0
    prof = ""
    pdf_name = ""
    duration = exam_dur
    date = ""
    exam_type = ""
    num_questions = sum_questions(pages)
    pages = pages
    school = "ubc"
    exam = Exam(num_pages, difficulty, prof, pdf_name, duration, date, exam_type, num_questions, exam_points, pages, school)
    exam.difficulty = 2 # rf.calc_exam_difficulty(exam)
    return exam


def sum_questions(pages):
    num_questions = 0
    for page in pages:
        num_questions += len(page.questions)
    return num_questions

from flask import (
    Blueprint, render_template
)
import json
from flaskr.exam import Exam, Page, Question
import flaskr.db as db
import flaskr.json_parser as json_parser

bp = Blueprint('json_translator', __name__)


@bp.route('/request')
def index():
    db.insert_default_school('uvic', 'victoria', 'canada')
    db.insert_alternate_school('uvic', 'university of victoria')

    db.insert_default_school('ubc', 'vancouver', 'canada')
    db.insert_alternate_school('ubc', 'university of british columbia')

    text_to_parse = open("file.json", "r")
    text = json.loads(text_to_parse.read())

    test = parse_pages(text)
    exam = create_exam(test)

    db.insert_full_exam(exam)
    exam = db.get_exam_db() # gets random exam from db
    return render_template('pages/testing_parser.html', test=test, exam=exam)


# returns a list of pages for a specific exam
def parse_pages(text):
    pages = text['pages']
    pages_list = []
    for page_idx, page in enumerate(pages):
        page_num = page['pageNumber']
        width = page['dimension']['width']
        height = page['dimension']['height']
        cur_page = Page(page_num, width, height)

        # get questions for this page
        cur_page.questions = parse_questions(text, page_idx, page_num)
        pages_list.append(cur_page)
    return pages_list


def parse_questions(text, page_idx, page_num):
    question_blocks = json_parser.get_question_blocks(text, page_idx)
    cur_questions = []
    for question_block in question_blocks:
        question_text = json_parser.get_question_text(text, question_block)
        difficulty = None
        page_num = page_num
        vertices = json_parser.get_question_bounds(question_block)
        question_type = None
        num_points = None
        exam_image = None #json_parser.extract_image(text, question_block)
        duration = None
        cur_question = Question(question_text, difficulty, page_num, vertices,
                                question_type, num_points, exam_image, duration)
        cur_questions.append(cur_question)
    return cur_questions


def create_exam(pages):
    num_pages = len(pages)
    difficulty = 0
    prof = ""
    pdf_name = ""
    duration = 0
    date = ""
    exam_type = ""
    num_questions = sum_questions(pages)
    pages = pages
    school = 0
    exam = Exam(num_pages, difficulty, prof, pdf_name, duration, date, exam_type, num_questions, pages, school)
    return exam


def sum_questions(pages):
    num_questions = 0
    for page in pages:
        num_questions += len(page.questions)
    return num_questions

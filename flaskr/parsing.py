from flask import (
    Blueprint, render_template
)
import json
from exam import Exam, Page
from flaskr.db import get_db

bp = Blueprint('parsing', __name__)


@bp.route('/request')
def index():
    db = get_db()
    test = parse_pages()
    insert_pages_db(test)
    pages_from_db = get_pages_db()
    return render_template('pages/testing_parser.html', test=test, pages_from_db=pages_from_db)


# returns a list of pages for a specific exam
def parse_pages():
    text_to_parse = open("file.json", "r")
    text = json.loads(text_to_parse.read())
    pages = text['pages']
    pages_list = []
    for page in pages:
        page_num = page['pageNumber']
        width = page['dimension']['width']
        height = page['dimension']['height']
        cur_page = Page(page_num, width, height)
        pages_list.append(cur_page)
    return pages_list

def create_exam():
    pages = parse_pages()
    num_pages = len(pages)
    difficulty = 0
    prof = ""
    pdf_name = ""
    duration = 0
    date = ""
    exam_type = ""
    #TODO: num_questions = sum_questions(pages)
    num_questions = 0
    exam = Exam(num_pages, difficulty, prof, pdf_name, duration, date, exam_type, num_questions, pages)
    return exam


def insert_exam_db(exam):
    db = get_db()
    db.execute(
        'INSERT INTO exam (num_pages, difficulty, prof, pdf_name, duration, date, exam_type, num_questions)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (exam.num_pages, exam.difficulty, exam.prof, exam.pdf_name, exam.duration, exam.date, exam.exam_type, exam.num_questions)
    )
    db.commit()


def get_exam_db():
    db = get_db()
    exam = db.execute(
        'SELECT num_pages, difficulty, prof, pdf_name, duration, date, exam_type, num_questions'
        ' FROM exam'
    ).fetchone()
    return exam

#TODO: Get/insert questions,course,school from/to db

def insert_pages_db(page_list):
    db = get_db()
    for page in page_list:
        db.execute(
            'INSERT INTO page (page_num, width, height)'
            ' VALUES (?, ?, ?)',
            (page.page_num, page.width, page.height)
        )
    db.commit()


def get_pages_db():
    db = get_db()
    pages = db.execute(
        'SELECT page_num, width, height'
        ' FROM page'
    ).fetchall()
    return pages


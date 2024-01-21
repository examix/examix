import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# DB Functions:

# Insert

def insert_full_exam(exam):
    insert_exam_db(exam)
    pages = exam.pages
    insert_pages_db(pages)
    for page in pages:
        questions = page.questions
        insert_questions_db(questions)


def insert_exam_db(exam):
    db = get_db()
    db.execute(
        'INSERT INTO exam (num_pages, difficulty, prof, pdf_name, duration, date, exam_type, num_questions, school_id)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (exam.num_pages, exam.difficulty, exam.prof, exam.pdf_name, exam.duration, exam.date, exam.exam_type, exam.num_questions, exam.school)
    )
    db.commit()


def insert_questions_db(question_list):
    db = get_db()
    for question in question_list:
        db.execute(
            'INSERT INTO question (question, difficulty, page_num, vertices, question_type, num_points, exam_image, duration, answer)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (question.question_text, question.difficulty, question.page_num, str(question.vertices),
             question.question_type, question.num_points, question.exam_image, question.duration, question.answer)
        )
    db.commit()


def insert_pages_db(page_list):
    db = get_db()
    for page in page_list:
        db.execute(
            'INSERT INTO page (page_num, width, height)'
            ' VALUES (?, ?, ?)',
            (page.page_num, page.width, page.height)
        )
    db.commit()

# Get


def get_exam_db():
    db = get_db()
    exam = db.execute(
        'SELECT num_pages, difficulty, prof, pdf_name, duration, date, exam_type, num_questions'
        ' FROM exam'
    ).fetchone()
    return exam


def get_questions_db():
    db = get_db()
    question = db.execute(
        'SELECT question_text, difficulty, page_num, vertices, question_type, num_points, exam_image, duration, answer'
        ' FROM question'
    ).fetchall()
    return question


def get_pages_db():
    db = get_db()
    pages = db.execute(
        'SELECT page_num, width, height'
        ' FROM page'
    ).fetchall()
    return pages


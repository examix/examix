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


def insert_default_school(name, city, country):
    db = get_db()
    try:
        db.execute(
            'INSERT INTO school (name, city, country)'
            ' VALUES (?, ?, ?)',
            (name, city, country)
        )
    except sqlite3.IntegrityError:
        pass
    db.commit()


def insert_alternate_school(default_name, alternate_name):
    db = get_db()
    try:
        db.execute(
            'INSERT INTO school_alternates (name, default_name)'
            ' VALUES (?, ?)',
            (alternate_name, default_name)
        )
    except sqlite3.IntegrityError:
        pass
    db.commit()


def insert_full_exam(exam, course_dept, course_num):
    insert_exam_db(exam, course_dept, course_num)


def insert_exam_db(exam, course_dept, course_num):
    db = get_db()
    course_id = db.execute('SELECT course_id FROM course WHERE department = ? AND code = ?', (course_dept, course_num)).fetchone()[0]
    db.execute(
        'INSERT INTO exam (num_pages, difficulty, prof, pdf_name, duration, exam_date, '
        'exam_type, num_questions, school_id, course_id, num_points)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (exam.num_pages, exam.difficulty, exam.prof, exam.pdf_name, exam.duration, exam.date, exam.exam_type,
         exam.num_questions, exam.school, course_id, exam.num_points)
    )
    exam_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
    print(exam_id)
    pages = exam.pages
    for page in pages:
        insert_page_db(page, exam_id)
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


def insert_question_db(question_list, page_id):
    db = get_db()
    for question in question_list:
        db.execute(
            'INSERT INTO question (question, difficulty, page_num, vertices, question_type, num_points, '
            'exam_image, duration, answer, page_id)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (question.question_text, question.difficulty, question.page_num, str(question.vertices),
             question.question_type, question.num_points, question.exam_image, question.duration, question.answer, page_id)
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


def insert_page_db(page, exam_id):
    db = get_db()
    db.execute(
        'INSERT INTO page (page_num, width, height, exam_id)'
        ' VALUES (?, ?, ?, ?)',
        (page.page_num, page.width, page.height, int(exam_id))
    )
    page_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
    questions = page.questions
    insert_question_db(questions, page_id)
    db.commit()


def insert_course_db(course):
    db = get_db()
    db.execute(
        'INSERT INTO course (department, code, name, description, school_id)'
        ' VALUES (?, ?, ?, ?, ?)',
        (course.department, course.course_code, course.course_name, course.description, course.school)
    )
    db.commit()


def insert_course_full_db(department, code, name, description, school):
    db = get_db()
    db.execute(
        'INSERT INTO course (department, code, name, description, school_id)'
        ' VALUES (?, ?, ?, ?, ?)',
        (department, code, name, description, school)
    )
    db.commit()


# Get

def get_schools():
    db = get_db()
    schools = db.execute(
        """SELECT name
        FROM school
        UNION 
        SELECT name
        FROM school_alternates"""
    ).fetchall()
    return schools


def get_exam_db(dept=None, course_number=None, school_name=None, prof=None):
    db = get_db()
    query = """SELECT num_pages, exam.course_id, difficulty, prof, pdf_name, duration, exam_date, exam_type, 
                    exam.num_questions, exam.school_id
                FROM exam
                JOIN school ON exam.school_id = school.name
                JOIN course ON exam.course_id = course.course_id
                WHERE exam.school_id = school.name"""

    # FULL OUTER JOIN course ON exam.course_id = course.course_id
    if dept is not None:
        query += " AND course.department = '" + dept + "'"
    if course_number is not None:
        query += " AND course.code = '" + course_number + "'"
    if school_name is not None:
        query += " AND school.name = '" + school_name + "'"
    if prof:
        query += " AND exam.prof = '" + prof + "'"
    print(query)
    exam = db.execute(query).fetchall()
    return exam

def get_exam_by_cid(course_id):
    db = get_db()
    exam = db.execute(
        """SELECT num_pages, exam.course_id, difficulty, prof, pdf_name, duration, exam_date, exam_type, 
                    exam.num_questions, exam.school_id
                FROM exam
                JOIN school ON exam.school_id = school.name
                JOIN course ON exam.course_id = course.course_id
                WHERE exam.course_id = ?""",
        (course_id,)
    ).fetchall()
    return exam

def get_questions_db():
    db = get_db()
   # question = db.execute(
   # """SELECT question, difficulty, question.page_num, vertices, question_type, num_points,
   #     exam_image, duration, answer
   #     FROM question JOIN page ON question.page_id = page.page_id
   #     WHERE page.exam_id = ?""",
   #     (exam_id,)
        'SELECT question, difficulty, page_num, vertices, question_type, num_points, exam_image, duration, answer'
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


def get_courses(department, course_code, school):
    db = get_db()
    query = """SELECT course_id, department, code, name, description, school_id
                FROM course
                WHERE department = '""" + department + "'"
    if course_code:
        query += " AND code = '" + course_code + "'"
    if school:
        query += " AND school_id = '" + school + "'"

    courses = db.execute(query).fetchall()
    return courses

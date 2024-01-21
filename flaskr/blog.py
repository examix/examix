from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import flaskr.db as db
import flaskr.search as searcher
import flaskr.json_translator as jt
import flaskr.json_parser as json_parser
import json
from flaskr.parse_document import process_document

bp = Blueprint('blog', __name__)
app = Flask(__name__)

@bp.route('/')
def index():
    return render_template('main/index.html')

# Routing
@bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        return redirect(url_for('blog.cards'), code=307)
    image_url = url_for('static', filename='styles/imgs/7.People-finder.svg')
    return render_template('main/search.html', image_url=image_url)

@bp.route('/remix')
def remix():
    return render_template('main/remix.html')

@bp.route('/cards', methods=['GET', 'POST'])
def cards():

    search_term = request.form['search']
    result_list = searcher.parse_search(search_term)
    dept = result_list[0]
    code = result_list[1]
    school = result_list[2]

    # query courses and exams
    courses = db.get_courses(dept, code, school)
    exams = db.get_exam_db(dept, code, school)

    course_list = []

    for course in courses:
        num = 0
        for exam in exams:
            if exam['course_id'] == course['course_id']:
                num += exam['num_questions']

        course_dict = {
            "course": course,
            "total_questions": num
        }
    
        course_list.append(course_dict)
    print(len(course_list))
    return render_template('main/cards.html', course_list=course_list, name=dept, code=code, uni=school)

@bp.route('/create', methods=['GET', 'POST'])
# @login_required
def create():
    image_url = url_for('static', filename='styles/imgs/10.Landscape.svg')
    if request.method == 'POST':
        file = request.files['fileUpload']
        text_to_parse = process_document(file)
        text = json.loads(text_to_parse.read())

        exam_dur = jt.json_parser.search_duration(text)
        exam_points = jt.json_parser.search_points(json_parser.get_intro_text(text['text']))
        test = jt.parse_pages(text, exam_points, exam_dur)
        exam = jt.create_exam(test, exam_points, exam_dur)

        db.insert_full_exam(exam)

        uni = request.form['university']
        course_dept = request.form['courseDept']
        course_num = request.form['courseNum']

        error = ""

        if file.filename == '' or not is_pdf(file):
            error = 'File is required. File must be of .pdf type.'
        elif not uni:
            error = 'University is required. Input must be alphabetic.'
        elif not course_dept:
            error = 'Course department is required. Input must be alphabetic '
        elif not course_num:
            error = 'Course Number is required. Input must be alphanumeric'

        if error is not None:
            flash(error)
        else:
            return redirect('/search')

    return render_template('main/create.html', image_url=image_url)

def is_pdf(file):
    # Check if the file content type is PDF
    if file.content_type == 'application/pdf':
        return True

    # Check if the file extension is PDF
    allowed_extensions = {'pdf'}
    return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions

def is_number(value):
    return value.isdigit()

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('main.index'))

    return render_template('main/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('main.index'))

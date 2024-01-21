from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import flaskr.db as db
import flaskr.search as searcher

bp = Blueprint('blog', __name__)
app = Flask(__name__)

@bp.route('/')
def index():
    image_url = url_for('static', filename='styles/imgs/10.Landscape.svg')
    return render_template('main/index.html', image_url=image_url)

# Routing
@bp.route('/search', methods=['GET', 'POST'])
# @login_required
def search():
    if request.method == 'POST':
        return redirect(url_for('blog.cards'), code=307)
        #return render_template('main/cards.html')
    image_url = url_for('static', filename='styles/imgs/7.People-finder.svg')
    return render_template('main/search.html', image_url=image_url)

@bp.route('/remix')
def remix():
    return render_template('main/remix.html')

@bp.route('/cards', methods=['GET', 'POST'])
def cards():
    # LIST OF COURSES WHICH MATCH CRITERIA FROM QUERY
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
    return render_template('main/cards.html', course_list=course_list, name='CSC', uni='UVIC')

@bp.route('/questions')
# @login_required
def questions():
    # LIST OF QUESTIONS
    questions = []
    questions_dict = []
    num = 1

    for question in questions: 
        dict = {
            "q_num": num,
            "type": question.question_type,
            "difficulty": question.difficulty,
            "description": question.question_text,
            "page_num": question.page_num,
            "points": question.num_points,
            "image": question.exam_image,
            "duration": question.duration
        }
        num += 1
    
        questions_dict.append(dict)

    return render_template('questions.html', dict = dict)

@bp.route('/create', methods=['GET', 'POST'])
# @login_required
def create():
    image_url = url_for('static', filename='styles/imgs/6.Effortless.svg')
    if request.method == 'POST':
        file = request.files['fileUpload']
        uni = request.form['university']
        courseDept = request.form['courseDept']
        courseNum = request.form['courseNum']

        error = ""

        if file.filename == '' or not is_pdf(file):
            error = 'File is required. File must be of .pdf type.'
        elif not uni:
            error = 'University is required. Input must be alphabetic.'
        elif not courseDept:
            error = 'Course department is required. Input must be alphabetic '
        elif not courseNum or is_number(courseNum):
            error = 'Couse Number is required. Input must be numeric'

        if error is not None:
            flash(error)
        else:
            # db = get_db()
            # db.execute(
            #     'INSERT INTO post (title, body, author_id)'
            #     ' VALUES (?, ?, ?)',
            #     (title, body, g.user['id'])
            # )
            # db.commit()
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

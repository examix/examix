from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import flaskr.db as db

bp = Blueprint('blog', __name__)
app = Flask(__name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('main/index.html', posts=posts)

# Routing
@bp.route('/search', methods=['GET', 'POST'])
# @login_required
def search():
    if request.method == 'POST':
       return redirect(url_for('blog.cards'))
        #return render_template('main/cards.html')
    image_url = url_for('static', filename='styles/imgs/7.People-finder.svg')
    return render_template('main/search.html', image_url=image_url)

@bp.route('/remix')
# @login_required
def remix():
    return render_template('main/remix.html')

@bp.route('/cards')
# @login_required
def cards():
    # LIST OF COURSES WHICH MATCH CRITERIA FROM QUERY
    #db.
    courses = []
    courses_dict = []

    for course in courses: 
        num = 0
        # NEED TO QUERY ALL THE EXAMS FOR A COURSE 
        exams = []
        for exam in exams: 
            if exam.department == course.department and exam.course_code == course.course_code:
                num += exam.num_questions
        dict = {
            "course": course,
            "total_questions": num
        }
    
        courses_dict.append(dict)

    return render_template('cards.html', dict = dict)

@bp.route('/create', methods=['GET', 'POST'])
# @login_required
def create():
    image_url = url_for('static', filename='styles/imgs/10.Landscape.svg')
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

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import flaskr.db as db
import flaskr.search as searcher
import flaskr.json_translator as jt
import flaskr.json_parser as json_parser
from flaskr.parse_document import process_document
from flask import render_template, redirect, url_for
import flaskr.remix_functions as rf

bp = Blueprint('blog', __name__)
app = Flask(__name__)

@bp.route('/')
def index():
    image_url = url_for('static', filename='styles/imgs/10.Landscape.svg')
    return render_template('main/index.html', image_url=image_url)


# Routing

@bp.route('/search', methods=['GET', 'POST'])
def search():
    ubc_image = url_for('static', filename='images/ubc.png')
    uvic_image = url_for('static', filename='images/uvic.png')

    if request.method == 'POST':
        search_result = request.form['search_result']

        parsed_result = searcher.parse_search(search_result)
        # parsed search query results
        dept = parsed_result[0]
        code = parsed_result[1]
        school_id = parsed_result[2]

        # get all the courses that match the search query
        courses = db.get_courses(dept, code, school_id)
        exams = db.get_exam_db(dept, code, school_id)

        # converting the list of courses to json
        course_array = []
        for course in courses:
            num = 0
            for exam in exams:
                if exam['course_id'] == course['course_id']:
                    num += exam['num_questions'] 

            course_dict = {
                "course_id" : course['course_id'],
                "department" : course['department'],
                "code" : course['code'],
                "name" : course['name'],
                "school_id" : course['school_id'],
                # "course" : dict(course),
                "num_questions": num
            }

            course_array.append(course_dict)

        return render_template('pages/search.html', course_array=course_array, ubc_image = ubc_image, uvic_image = uvic_image)
    
    course_array = db.get_all_courses()
    
    return render_template('pages/search.html', course_array=course_array, ubc_image = ubc_image, uvic_image = uvic_image)












@bp.route('/course', methods=['GET', 'POST'])
def course():

    class Person:
        def __init__(self, name, age, extra_info):
            self.name = name
            self.age = age
            self.extra_info = extra_info

    # Sample data
    persons_data = [
        Person("John", 25, "Extra information for John"),
        Person("Jane", 30, "Extra information for Jane"),
        # Add more data as needed
    ]
    image_url = url_for('static', filename='images/ubc.png')
    image_url2 = url_for('static', filename='images/uvic.png')
    persons = []
    return render_template('main/test-child-2.html', image_url=image_url, image_url2=image_url2, persons = persons_data)










# @bp.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         return redirect(url_for('blog.cards'), code=307)
#     image_url = url_for('static', filename='styles/imgs/7.People-finder.svg')
#     return render_template('main/search.html', image_url=image_url)

@bp.route('/remix', methods=['GET', 'POST'])
def remix():
    if request.method == 'POST':
        return redirect(url_for('blog.remix_result'), code=307)
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

    return render_template('main/cards.html', course_list=course_list, name=dept, code=code, uni=school)

@bp.route('/exams', methods=['POST', 'GET'])
def exams():
        # output exams to questions     
    department = request.args.get('department')
    code = request.args.get('code')
    school = request.args.get('school')
    prof = request.args.get('prof')

    # list of exams for one course given course_id
    exams = db.get_exam_db(department, code, school, prof)

    list_exams = []
    num = 1

    for exam in exams:
        exam_dict = {
            "exam_id": num,
            "num_pages": exam["num_pages"],
            "difficulty": exam["difficulty"],
            "duration": exam["duration"],
            "num_questions": exam["num_questions"],
            "num_points": 0,  # Optional attribute, defaulting to None if not present
            "pages": '',
            "school": '',
            "department": '',
            "course_code": 0
        }
        num += 1
        list_exams.append(exam_dict)

    return render_template('main/exams.html', list_exams=list_exams, name=department, code=code, uni=school)

@bp.route('/remixresults', methods = ['GET', 'POST'])
def remix_result():
    time = int(request.form['time'])
    #diff = float(request.form['customRange'])
    #questions = db.get_questions_db(1)
    #johns question functoin
    questions, exam_time, exam_difficulty = rf.remix(int(time), 2.5)
    questions_list = []
    num = 1

    for question in questions:
        question_dict = {
            "q_num": num,
            "type": question['question_type'],
            "difficulty": question['difficulty'],
            "description": question['question'],
            "page_num": question['page_num'],
            "points": question['num_points'],
            "image": question['exam_image'],
            "duration": question['duration'],
            "description_short": question['question'][:25] + "..."  + question['question'][50:75] if len(question['question']) > 75 else question['question']
        }
        num += 1

        questions_list.append(question_dict)

    return render_template('main/remix_questions.html', questions_list=questions_list)

@bp.route('/questions', methods = ['GET', 'POST'])
# @login_required
def questions():
    # LIST OF QUESTIONS
    #exam_id = request.form['exam_id']
    #card_num = 0 # note same as exam_num

    exam_id = request.args.get('exam_id')
    questions = db.get_questions_db(exam_id)
    questions_list = []
    num = 1

    for question in questions: 
        question_dict = {
            "q_num": num,
            "type": question['question_type'],
            "difficulty": question['difficulty'],
            "description": question['question'],
            "page_num": question['page_num'],
            "points": question['num_points'],
            "image": question['exam_image'],
            "duration": question['duration'],
            "description_short": question['question'][:25] + "..."  + question['question'][50:75] if len(question['question']) > 75 else question['question']
        }
        num += 1
    
        questions_list.append(question_dict)

    return render_template('main/questions.html', questions_list=questions_list)

@bp.route('/create', methods=['GET', 'POST'])
# @login_required
def create():
    image_url = url_for('static', filename='styles/imgs/6.Effortless.svg')
    if request.method == 'POST':
        file = request.files['fileUpload']
        text_to_parse = process_document(file)
        text = text_to_parse
            #json.loads(text_to_parse))
    
        exam_dur = jt.json_parser.search_duration(text)
        exam_points = jt.json_parser.search_points(json_parser.get_intro_text(text['text']))
        pages = jt.parse_pages(text, exam_points, exam_dur)
        exam = jt.create_exam(pages, exam_points, exam_dur)
        course_dept = request.form['courseDept'].upper()
        course_num = request.form['courseNum']

        db.insert_full_exam(exam, course_dept, course_num)

        uni = request.form['university']

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



from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    image_url2 = url_for('static', filename='styles/imgs/10.Landscape.svg')
    return render_template('main/index.html', image_url2=image_url2)

# Routing
@bp.route('/search')
# @login_required
def search():
    image_url = url_for('static', filename='styles/imgs/2.Searching.svg')
    return render_template('main/search.html', image_url=image_url)

@bp.route('/remix')
# @login_required
def remix():
    return render_template('main/remix.html')

@bp.route('/cards')
# @login_required
def cards():
    image_url = url_for('static', filename='styles/imgs/20.Searching.svg')
    name = 'CSC'
    uni = 'University of Victoria'
    return render_template('main/cards.html', name=name, uni = uni, )

@bp.route('/create')
# @login_required
def create():
    image_url = url_for('static', filename='styles/imgs/20.Searching.svg')
    return render_template('main/create.html', image_url=image_url)
    # if request.method == 'POST':
    #     title = request.form['title']
    #     body = request.form['body']
    #     error = None

    #     if not title:
    #         error = 'Title is required.'

    #     if error is not None:
    #         flash(error)
    #     else:
    #         db = get_db()
    #         db.execute(
    #             'INSERT INTO post (title, body, author_id)'
    #             ' VALUES (?, ?, ?)',
    #             (title, body, g.user['id'])
    #         )
    #         db.commit()
    #         return redirect(url_for('main.index'))

    # return render_template('main/create.html')

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

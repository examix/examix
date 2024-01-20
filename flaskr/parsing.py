from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import json
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('parsing', __name__)


@bp.route('/request')
def index():
    db = get_db()
    #TODO: Call parse here, send JSON through
    test = parse_pages()
    return render_template('pages/testing_parser.html', test=test)

def parse_pages():
    text_to_parse = open("file.json", "r")
    text = json.loads(text_to_parse.read())
    pages = text['pages']

    return text['pages'][0]['pageNumber']


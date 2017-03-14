"""
    minesweeper.main
    ~~~~~~~~~~~~~~~~~~~~~~~
    
    Description
    
    :copyright: (c) 2017 by LeCoVi.
    :author: Leandro E. Colombo Viña <colomboleandro at bitson.com.ar>.
    :license: AGPL, see LICENSE for more details.
"""
# Standard lib imports
# Third-party imports
from flask import Flask
# LeCoVi imports
from app.routes import mines
from app.models import db


app = Flask(__name__)
app.config['SECRET_KEY'] = '70p 53cr37'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minesweeper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(mines)
db.init_app(app)

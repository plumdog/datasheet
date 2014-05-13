from flask import Flask, render_template, request, redirect, flash, url_for, abort
from flask.ext.login import LoginManager, login_user, current_user, logout_user, login_required, login_url
from .models import db, User
from .forms import LoginForm
from .db_functions import get_all_tables, get_table_obj, engine, run_sql
from .data_types import data_factory

from flask_debugtoolbar import DebugToolbarExtension
from flask_table import Table as HTMLTable, Col, LinkCol

import config_combined

def string_isinstance(obj, cls_name):
    return cls_name in [type_.__name__ for type_ in obj.__class__.__bases__] + [type(obj).__name__]

def app_factory(**kwargs):
    app = Flask(__name__)
    app.config.from_object(config_combined)
    db.init_app(app)

    DebugToolbarExtension(app)

    app.add_template_global(string_isinstance, name='string_isinstance')

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        form = LoginForm(request.form)
        if form.validate_on_submit():
            if (form.username.data == app.config['ADMIN_USERNAME'] and
                form.password.data == app.config['ADMIN_PASSWORD']):
                user = User()
                login_user(user)
                return redirect(url_for('index'))
            else:
                form.username.errors.append('Invalid Username...')
                form.password.errors.append('...or Password')
        return render_template('login.html', form=form)

    @app.route('/logout/')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/content/')
    @login_required
    def content():
        return render_template('content.html')

    @app.errorhandler(404)
    def err404(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def err500(e):
        return render_template('500.html'), 500

    @app.route('/all-tables/')
    def all_tables():
        class TableTable(HTMLTable):
            name = LinkCol('Name', 'table', attr='name', url_kwargs=dict(table_name='name'))
        t = TableTable(get_all_tables(app.config['SQLALCHEMY_DATABASE_URI']))
        return t.__html__()

    @app.route('/table/<string:table_name>/')
    def table(table_name):
        table_obj = get_table_obj(app.config['SQLALCHEMY_DATABASE_URI'], table_name)
        q = table_obj.select()
        out = list(run_sql(q, app.config['SQLALCHEMY_DATABASE_URI'], as_text=False))

        html_table = HTMLTable(out)
        for c in table_obj.columns:
            d = data_factory(sql_type=str(c.type))
            html_table._cols[c.name] = d.col(c.name.title())

        return html_table.__html__()

    # use: http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/automap.html

    ## db manipulations
    @app.route('/create/')
    def create():
        run_sql(
            ('CREATE TABLE test ('
             'id INTEGER NOT NULL AUTO_INCREMENT, '
             'name VARCHAR(100), '
             'PRIMARY KEY (id)'
             ');'),
            app.config['SQLALCHEMY_DATABASE_URI']
        )
        return redirect(url_for('index'))


    return app

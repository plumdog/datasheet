from flask import Blueprint, request, render_template, redirect, current_app, url_for
from .forms import TableForm, ColumnForm
from .sql import create, add_cols
from .db_functions import run_sql, get_table_obj
from .data_types import str_data_factory


def bp_factory():
    bp = Blueprint('table_bp', __name__, template_folder='templates')

    @bp.route('/add/', methods=['GET', 'POST'])
    def add():
        form = TableForm(request.form)
        if form.validate_on_submit():
            sql = create(form.name.data)
            run_sql(sql, current_app.config['SQLALCHEMY_DATABASE_URI'])
            return redirect(url_for('all_tables'))
        return render_template('table_add.html', form=form)

    @bp.route('/add-col/<string:table>', methods=['GET', 'POST'])
    def add_col(table):
        form = ColumnForm(request.form)
        table = get_table_obj(current_app.config['SQLALCHEMY_DATABASE_URI'], table)

        if form.validate_on_submit():
            name = form.name.data
            data_type_name = form.data_type.data
            cols = [(name, str_data_factory(data_type_name))]
            sql = add_cols(table.name, cols)
            print(sql)
            run_sql(sql, current_app.config['SQLALCHEMY_DATABASE_URI'])
            return redirect(url_for('all_tables'))
        return render_template('table_col_add.html', form=form, table_name=table.name)
    return bp

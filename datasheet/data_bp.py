from flask import Blueprint, current_app, request, render_template, redirect, url_for, abort
from flask_table import Table as HTMLTable, LinkCol as _LinkCol, ButtonCol as _ButtonCol
from .data_types import data_factory
from .forms import form_factory

from .db_functions import get_table_obj, engine, run_sql, table_query

class LinkCol(_LinkCol):
    def __init__(self, *args, **kwargs):
        url_extra_kwargs = kwargs.pop('url_extra_kwargs', {})
        _LinkCol.__init__(self, *args, **kwargs)
        self._url_extra_kwargs = url_extra_kwargs

    def url_kwargs(self, item):
        url_kwargs_out = _LinkCol.url_kwargs(self, item)
        url_kwargs_out.update(self._url_extra_kwargs)
        return url_kwargs_out

class ButtonCol(_ButtonCol):
    def __init__(self, *args, **kwargs):
        url_extra_kwargs = kwargs.pop('url_extra_kwargs', {})
        _ButtonCol.__init__(self, *args, **kwargs)
        self._url_extra_kwargs = url_extra_kwargs

    def url_kwargs(self, item):
        url_kwargs_out = _ButtonCol.url_kwargs(self, item)
        url_kwargs_out.update(self._url_extra_kwargs)
        return url_kwargs_out

def _get_table(table_name):
    return get_table_obj(current_app.config['SQLALCHEMY_DATABASE_URI'], table_name)

def _get_cols(table_obj, include_primary_keys=False):
    for c in table_obj.columns:
        if (not c.primary_key) or include_primary_keys:
            yield (c.name, data_factory(sql_type=str(c.type)))

def _get_pk_cols(table_obj):
    return table_obj.primary_key.columns

def bp_factory():
    bp = Blueprint('data_bp', __name__, template_folder='templates')

    @bp.route('/view/<string:table>/')
    def view(table):
        table_obj = _get_table(table)
        q = table_obj.select()
        out = list(run_sql(q, current_app.config['SQLALCHEMY_DATABASE_URI'], as_text=False))

        html_table = HTMLTable(out)
        for name, d in _get_cols(table_obj):
            html_table._cols[name] = d.col(name.title())
        from pprint import pprint

        pks_col_names = {c.name: c.name for c in _get_pk_cols(table_obj)}
        html_table._cols['_edit'] = LinkCol('Edit', '.edit', url_kwargs=pks_col_names, url_extra_kwargs=dict(table=table))
        html_table._cols['_delete'] = ButtonCol('Delete', '.delete', url_kwargs=pks_col_names, url_extra_kwargs=dict(table=table))

        return render_template('data_view.html', t=html_table)

    @bp.route('/add/<string:table>/', methods=['GET', 'POST'])
    def add(table):
        table_obj = _get_table(table)
        f = form_factory(_get_cols(table_obj))(request.form)
        if f.validate_on_submit():
            q = table_obj.insert().values(**f.data)
            run_sql(q, current_app.config['SQLALCHEMY_DATABASE_URI'], as_text=False)
            return redirect(url_for('.view', table=table))
            
        return render_template('data_add.html', f=f)

    def _filter(table_obj, args):
        return [getattr(_get_pk_cols(table_obj), k) == v for k,v in args.items()]

    def _load(table_obj, args):
        q = table_obj.select().where(*_filter(table_obj, request.args))
        out = list(run_sql(q, current_app.config['SQLALCHEMY_DATABASE_URI'], as_text=False))

        print(out)

        if len(out) == 0:
            abort(404)
        elif len(out) > 1:
            abort(500)

        return out[0]


    @bp.route('/edit/<string:table>/', methods=['GET', 'POST'])
    def edit(table):
        table_obj = _get_table(table)
        row = _load(table_obj, request.args)

        f = form_factory(_get_cols(table_obj))(request.form, obj=row)
        if f.validate_on_submit():
            q = table_obj.update().where(*_filter(table_obj, request.args)).values(**f.data)
            run_sql(q, current_app.config['SQLALCHEMY_DATABASE_URI'], as_text=False)
            return redirect(url_for('.view', table=table))
            
        return render_template('data_edit.html', f=f)

    @bp.route('/delete/<string:table>/', methods=['POST'])
    def delete(table):
        table_obj = _get_table(table)
        row = _load(table_obj, request.args)

        q = table_obj.delete().where(*_filter(table_obj, request.args))
        run_sql(q, current_app.config['SQLALCHEMY_DATABASE_URI'], as_text=False)
        
        return redirect(url_for('.view', table=table))

    return bp

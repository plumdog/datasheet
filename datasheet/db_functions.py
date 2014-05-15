from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker


def get_all_tables(con_str):
    special_tables = ['user', 'alembic_version']
    table_names = [{'name': r[0]} for r in run_sql('SHOW TABLES', con_str)
                   if r[0] not in special_tables]
    return table_names


def get_table_obj(con_str, table_name):
    meta = MetaData()
    tab = Table(table_name, meta, autoload=True, autoload_with=engine(con_str))
    return tab


def engine(connection_str):
    return create_engine(connection_str)


def run_sql(sql, connection_str, args={}, as_text=True):
    if as_text:
        
        sql = text(sql % args)

    conn = engine(connection_str).connect()
    out = conn.execute(sql)
    return out

def session(connection_str):
    
    Session = sessionmaker(bind=engine(connection_str))
    return Session()

def table_query(connection_str, table):
    return session(connection_str).query(table)

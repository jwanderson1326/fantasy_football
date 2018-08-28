'''Functions for manipulating the lookup DB'''
import os
import csv
import mysql.connector
from .db_config import HOST, USER, DB, PASSWD, PATH_CSV


def connect_to_db():
    '''Connecting to mysql database'''
    db = mysql.connector.connect(host = HOST,
                         user = USER,
                         passwd = PASSWD,
                         db = DB)
    return db


def format_schema_query(schema, primary_key, name):
    '''Formatting query to create a table'''
    columns = []
    for i in schema.keys():
        if i == primary_key:
            col = "%s %s PRIMARY KEY" % (i, schema[i])
        else:
            col = "%s %s" % (i, schema[i])
        columns.append(col)
    query = "CREATE TABLE %s (" % name  + ','.join(columns) + ")"
    return query


def insert_csv_query(table):
    '''Formatting query to insert csv'''
    columns = []
    values = []
    db = connect_to_db()
    curs = db.cursor()
    curs.execute("SHOW COLUMNS from %s" % table)
    for column in curs.fetchall():
        columns.append(column[0])
        if 'int' in column[1]:
            values.append('%s')
        else:
            values.append('%s')
    string = "INSERT INTO %s(" % table + ','.join(columns) +") VALUES(" + ','.join(values) + ")"
    return string


def create_table(schema, primary_key, name):
    '''Create table function'''
    db = connect_to_db()
    curs = db.cursor()
    query = format_schema_query(schema, primary_key, name)
    curs.execute(query)
    db.commit()
    curs.close()


def drop_table(name):
    '''Drop table function'''
    db = connect_to_db()
    curs = db.cursor()
    curs.execute("DROP TABLE %s" % name)


def insert_csv(file, table):
    '''For appending onto files'''
    db = connect_to_db()
    curs = db.cursor()
    query = insert_csv_query(table)
    csv_loc = os.path.join(PATH_CSV, file)
    with open(csv_loc, 'r') as csvfile:
        csv_data = csv.reader(csvfile)
        next(csv_data)
        for row in csv_data:
            curs.execute(query, row)
    db.commit()
    curs.close()


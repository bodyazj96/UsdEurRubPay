import sqlite3
from sqlite3 import Error
from flask import request
import datetime


def create_connection(db_file):

    conn = None

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def insert_data_to_db(conn, payer_request):

    payer_request = (request.form['currency'], request.form['payment_amount'], datetime.datetime.now(), request.form['item_description'], payer_request['shop_order_id'])

    sql = ''' INSERT INTO payer_request(currency,amount,request_time,item_description,shop_order_id)
              VALUES(?,?,?,?,?) '''

    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, payer_request)
        conn.commit()

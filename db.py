import sqlite3
import logging

logger = logging.getLogger(__name__)

conn = sqlite3.connect('griddy.db')


def create_table():
    cursor = conn.cursor()
    try:
        cursor.execute(''' CREATE TABLE PRICES (
        ID INTEGER PRIMARY KEY,
        DATE TEXT NOT NULL,
        HOUR_NUM TEXT NOT NULL,
        MIN_NUM TEXT NOT NULL,
        SETTLEMENT_POINT TEXT NOT NULL,
        PRICE_TYPE TEXT NOT NULL,
        PRICE_CKWH TEXT NOT NULL,
        VALUE_SCORE TEXT NOT NULL,
        MEAN_PRICE_CKWH TEXT NOT NULL,
        DIFF_MEAN_CKWH TEXT NOT NULL,
        HIGH_CKWH TEXT NOT NULL,
        LOW_CKWH TEXT NOT NULL,
        STD_DEV_CKWH TEXT NOT NULL,
        PRICE_DISPLAY TEXT NOT NULL,
        PRICE_DISPLAY_SIGN TEXT NOT NULL,
        DATE_LOCAL_TZ TEXT NOT NULL
        ); ''')
    except Exception as e:
        logger.exception(f"create table error {e}")
    cursor.close()


def add_data (date, hour_num, min_num, settlement_point, price_type, price_ckwh, value_score,
mean_price_ckwh, diff_mean_ckwh, high_ckwh, low_ckwh, std_dev_ckwh, price_display,
price_display_sign, date_local_tz):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO PRICES values(NULL, (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?))", (date, hour_num, min_num, settlement_point, price_type, price_ckwh, value_score,
                 mean_price_ckwh, diff_mean_ckwh, high_ckwh, low_ckwh, std_dev_ckwh, price_display,
                 price_display_sign, date_local_tz))
    conn.commit()
    cursor.close()

def fetch_data():
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM PRICES"):
        print(f"data row {row}")
    cursor.close()


def fetch_current_data(current_date):
    cursor = conn.cursor()
    for row in cursor.execute("SELECT * FROM PRICES WHERE date=(?)", (current_date,)):
        print(f"current row {row}")
    cursor.close()

def check_tables():
    cursor = conn.cursor()
    if cursor:
        tables = cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='prices' ''')
        print(f"cursor check {tables}")
        cursor_data = cursor.fetchone()
        cursor.close()
        return cursor_data

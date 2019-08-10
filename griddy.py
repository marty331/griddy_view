from abc import ABC
import requests
import sqlite3
import datetime
import logging

import db
from cfg import CFG

logger = logging.getLogger(__name__)

class Griddy(ABC):
    def __init__(self, date, hour_num, min_num, settlement_point, price_type, price_ckwh, value_score, mean_price_ckwh, diff_mean_ckwh, high_ckwh, low_ckwh, std_dev_ckwh, price_display, price_display_sign, date_local_tz):
        self.date = date
        self.hour_num = hour_num
        self.min_num = min_num
        self.settlement_point = settlement_point
        self.price_type = price_type
        self.price_ckwh = price_ckwh
        self.value_score = value_score
        self.mean_price_ckwh = mean_price_ckwh
        self.diff_mean_ckwh = diff_mean_ckwh
        self.high_ckwh = high_ckwh
        self.low_ckwh = low_ckwh
        self.std_dev_ckwh = std_dev_ckwh
        self.price_display = price_display
        self.price_display_sign = price_display_sign
        self.date_local_tz = date_local_tz

    def print_current_data(self):
        print(f"date {self.date}")
        print(f"price {self.price_display} {self.price_display_sign}")

    def get_all_data(self):
        db.fetch_data()

    def get_current_data(self, date):
        current_data = db.fetch_current_data(date)
        logger.info(f"current data {current_data}")
        return current_data

    def save_data(self):
        if not self.get_current_data(self.date):
            saved_row = db.add_data(self.date, self.hour_num, self.min_num, self.settlement_point, self.price_type,
            self.price_ckwh, self.value_score, self.mean_price_ckwh, self.diff_mean_ckwh, self.high_ckwh, self.low_ckwh,
            self.std_dev_ckwh, self.price_display, self.price_display_sign, self.date_local_tz)
            logger.info(f"saved data {saved_row}")


def get_griddy():
    griddly_url = "https://app.gogriddy.com/api/v1/insights/getnow"

    data = {
    	"settlement_point": CFG.SETTLEMENT_POINT,
    }
    griddy_data = requests.post(griddly_url, json=data).json()
    print(griddy_data['now']['date'])
    current_griddy = Griddy(
    date=griddy_data['now']['date'],
    hour_num=griddy_data['now']['hour_num'],
    min_num=griddy_data['now']['min_num'],
    settlement_point=griddy_data['now']['settlement_point'],
    price_type=griddy_data['now']['price_type'],
    price_ckwh=griddy_data['now']['price_ckwh'],
    value_score=griddy_data['now']['value_score'],
    mean_price_ckwh=griddy_data['now']['mean_price_ckwh'],
    diff_mean_ckwh=griddy_data['now']['diff_mean_ckwh'],
    high_ckwh=griddy_data['now']['high_ckwh'],
    low_ckwh=griddy_data['now']['low_ckwh'],
    std_dev_ckwh=griddy_data['now']['std_dev_ckwh'],
    price_display=griddy_data['now']['price_display'],
    price_display_sign=griddy_data['now']['price_display_sign'],
    date_local_tz=griddy_data['now']['date_local_tz'])
    return current_griddy

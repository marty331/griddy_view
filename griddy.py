#!/usr/bin/env python

from abc import ABC
import requests
import sqlite3
import datetime
import logging

import db
import alert_state
import messages

from datetime import datetime

from cfg import CFG

logging.basicConfig(filename="griddy.log",
                            filemode='a',
                            format="%(asctime)s:%(levelname)s:%(message)s",
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

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

    def logger.info_current_data(self):
        logger.info(f"date {self.date}")
        logger.info(f"price {self.price_display} {self.price_display_sign}")

    def get_all_data(self):
        db.fetch_data()

    def create_table(self):
        db.create_table()

    def get_current_data(self, date):
        current_data = db.fetch_current_data(date)
        logger.info(f"current data {current_data}")
        return current_data

    def save_data(self):
        logger.info(f"current row {self.get_current_data(self.date)}")
        logger.info(f"date {self.date}")
        logger.info(f"local date {self.date_local_tz}")
        datetime_object = datetime.strptime(self.date, '%Y-%m-%dT%H:%M:%SZ')
        datetime_object_local = datetime.strptime(self.date_local_tz, '%Y-%m-%dT%H:%M:%S%z')
        logger.info(f"datetime object {datetime_object}")
        logger.info(f"datetime local {datetime_object_local}")
        if not self.get_current_data(self.date):
            send_new_alert = self.alert_send_check()
            if send_new_alert[0]:
                messages.send_message(send_new_alert[1], CFG.TO_NUMBERS)
            saved_row = db.add_data(datetime_object, self.hour_num, self.min_num, self.settlement_point, self.price_type,
            self.price_ckwh, self.value_score, self.mean_price_ckwh, self.diff_mean_ckwh, self.high_ckwh, self.low_ckwh,
            self.std_dev_ckwh, self.price_display, self.price_display_sign, datetime_object_local)
            logger.info(f"saved data {saved_row}")
        else:
            logger.info(f"row exists")

    def alert_send_check(self):
        current_alert_state = alert_state.get_alert_state()
        logger.info(f"current alert state {current_alert_state}")
        if float(self.price_display) >= float(CFG.ALERT_STATE_VALUE):
            logger.info(f"High Price Alert! {self.price_display} {self.price_display_sign}")
            if current_alert_state == 0:
                logger.info(f"Send High Price alert {current_alert_state}")
                alert_state.change_state(1)
                return (True, f"Griddy high price alert! {self.price_display} {self.price_display_sign}")
        else:
            if current_alert_state == 1:
                logger.info(f"Prices lowered alert {current_alert_state}")
                alert_state.change_state(0)
                return (True, "Griddy price spike has ended.")
        return (False, None)

    def close(self):
        db.close_connection()


def get_griddy():
    griddly_url = "https://app.gogriddy.com/api/v1/insights/getnow"

    data = {
    	"settlement_point": CFG.SETTLEMENT_POINT,
    }
    griddy_data = requests.post(griddly_url, json=data).json()
    logger.info(griddy_data['now']['date'])
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


if __name__ == "__main__":
    griddy = get_griddy()
    griddy.create_table()
    griddy.save_data()
    griddy.close()

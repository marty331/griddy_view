# Griddy View
Look up prices for Griddy electrical service in your region, then track and view over time.

I build this application to run on a Raspberry Pi, but it should run on any Linux/Unix system.  I have a cron job that runs every 5 minutes to check the price of electricity with Griddy.  The prices are logged in a SQLite3 database (future use will be to display in a web front end) and if the price is higher/lower than the self configured spike amount the application will send an SMS notification to a list of recipients.

## Configuration values
The application requires several configuration values that should be placed in the root of the project in a .env file.  The cfg.py file will read these values and import them into the app.

SETTLEMENT_POINT=<LZ_SOME_AREA>

METERID=<YOUR_METER_NUMBER>

MEMBERID=<YOUR_GRIDDY_ACCOUNT_NUMBER>

ALERT_STATE_VALUE=<YOUR_SPIKE_NUMBER> Example: 12.5

ACCOUNT_SID=<YOUR_TWILIO_ACCOUNT_SID>

AUTH_TOKEN=<YOUR_TWILIO_AUTH_TOKEN>

FROM_NUMBER=<YOUR_TWILIO_SEND_NUMBER>

TO_NUMBERS=<COMMA_SEPERATED_PHONE_NUMBER_LIST> Example: 8005551212,8885551212

COST_PERIOD=2019-08-01  Future Use - Not Required

COST_INTERVAL=monthly Future Use - Not Required

## Cron Job
Create a cron job by going to the terminal on the Raspberry Pi and running the following command:  crontab -e
Scroll to the bottom of the file and on a blank line at the bottom of the file enter the following:

*/5 * * * * cd /home/pi/griddy_view && /usr/local/bin/python3.7 griddy.py

## Install Python 3.7
I followed the following guide for installing Python on the Raspberry Pi
 [Install Python on Raspberry Pi](https://installvirtual.com/install-python-3-7-on-raspberry-pi/)

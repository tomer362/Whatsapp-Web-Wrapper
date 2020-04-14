# *-* coding: utf-8 *-*
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta

from whatsapp_web_wrapper import WhatsappWeb


def main():
    with WhatsappWeb() as whatsapp_web:
        whatsapp_web.add_message_schedule("אני", 'HELLO WORLD', trigger=IntervalTrigger(seconds=1, jitter=10))
        input("WAIT...")


if __name__ == '__main__':
    main()

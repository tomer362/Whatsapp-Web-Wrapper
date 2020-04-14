from threading import Lock
from typing import Union

from client import Contact

from apscheduler.schedulers.background import BackgroundScheduler

from client import Message
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from selenium import webdriver

WHATSAPP_WEB_URL = 'https://web.whatsapp.com/'


class WhatsappWeb:
    """
    Whatsapp Web wrapper class
    """

    def __init__(self):
        """
        Initializes whatsapp web driver and the scheduler for async tasks.
        """

        self.web_driver = webdriver.Firefox()
        self.web_driver.get(WHATSAPP_WEB_URL)

        self.__web_lock = Lock()
        self.__scheduler = BackgroundScheduler()
        self.__scheduler.start()

        input("Connect with your phone and then click enter..")

    @property
    def web_lock(self):
        """
        @return: Returns threading lock
        @rtype: Lock
        """
        return self.__web_lock

    def add_message_schedule(self, contact_name, message_obj, trigger):
        """
        Adds a periodic/once message send function.
        @param contact_name: Contact's name
        @type contact_name: C{str}
        @param message_obj: Message object. can contain multiple layers of information (text/media)
        @type message_obj: Message
        @param trigger: APScheduler trigger object.
        @type trigger: Union[CronTrigger, IntervalTrigger, DateTrigger]
        """

        contact = Contact(contact_name, self)
        self.__scheduler.add_job(contact.send_message, trigger=trigger, args=[message_obj])

    def __close(self):
        """
        Close operation for the whatsapp web wrapper, cleans resources and kills all jobs.
        """

        self.web_driver.close()
        self.web_driver.quit()

        if self.__scheduler.running:
            self.__scheduler.shutdown(wait=False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

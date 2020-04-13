from threading import Lock

from apscheduler.schedulers.background import BackgroundScheduler
from selenium import webdriver

from client import Contact

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

        input("Connect with your phone and then click enter..")

    @property
    def web_lock(self):
        """
        @return: Returns threading lock
        @rtype: Lock
        """
        return self.__web_lock

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

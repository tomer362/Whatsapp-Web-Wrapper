from apscheduler.schedulers.background import BackgroundScheduler
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
        self.__lock = False
        self.__scheduler = BackgroundScheduler()

        input("Connect with your phone and then click enter..")

    @property
    def lock(self):
        return self.__lock

    @lock.setter
    def lock(self, value):
        """
        @type value: C{bool}
        """
        self.__lock = value

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

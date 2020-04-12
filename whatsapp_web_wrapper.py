import time

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
        self.__driver = webdriver.Firefox()
        self.__driver.get(WHATSAPP_WEB_URL)
        self.__scheduler = BackgroundScheduler()

        input("Connect With your phone and then click enter..")

    def navigate_to_contact_chat(self, contact_name):
        """
        Click's on the first contact that matches the contact name given. waits
        @param contact_name: Contact's name
        @type contact_name: C{str}
        """
        # Find the root of the contact search bar so we can focus on it by clicking.
        root_contacts_search_bar = self.__driver.find_elements_by_xpath("//div[contains(@class, '_3F6QL _3xlwb')]")[0]
        root_contacts_search_bar.click()

        # Find the contact search bar text div
        contact_search_bar = root_contacts_search_bar.find_elements_by_xpath(
            "./div[contains(@class, 'copyable-text selectable-text')]"
        )[0]

        # Type the contact's name in the search bar
        contact_search_bar.send_keys(contact_name)

        # Wait for the search to work for sure
        # TODO: make it smart by searching for the search looping icon and if it disappeares it mean the search ended
        #  (or some other form of ending of search).
        time.sleep(3)

        # Whatsapp randomizes the order of the divs in the panel of contacts so we need to get the order by location
        # in y axis
        contact_elems_sorted_by_y_loc = sorted(
            self.__driver.find_elements_by_xpath("//div[@id='side']//div[@id='pane-side']/div/div/div/div"),
            key=lambda x: x.location['y'])
        contact_elems_sorted_by_y_loc[1].click()

        # Waits for the chat with the contact to open.
        time.sleep(2)

    def send_message(self, contact_name, message, should_navigate_first=False):
        """
        Sends message to a specific user. the user decides if should navigate to the contact chat or if he is
        already in that contact's chat page.
        @type contact_name: C{str}
        @param message: Chat message buffer
        @type message: C{str}
        @param should_navigate_first: Should navigate to contact's chat page first.
        @type should_navigate_first: C{bool}
        """
        if should_navigate_first:
            self.navigate_to_contact_chat(contact_name)

        chat_text_box_elem = self.__driver.find_element_by_xpath(
            "//div[@id='main']//div[contains(@class, 'copyable-text selectable-text')]"
        )
        chat_text_box_elem.click()
        chat_text_box_elem.send_keys(message)

        # Wait for send button to be created
        time.sleep(0.4)

        # Find the send button and click it (by finding the send icon first and then going up to the button)
        send_button_elem = self.__driver.find_element_by_xpath("//div[@id='main']//footer//span[@data-icon='send']/..")
        send_button_elem.click()

    def __close(self):
        """
        Close operation for the whatsapp web wrapper, cleans resources and kills all jobs.
        """
        self.__driver.close()
        self.__driver.quit()
        self.__scheduler.shutdown(wait=False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()


class Contact:
    """
    Class represents an entity that can be interacted by chat,
    it can be a group or a private chat
    """
    pass

# class WhatsappMessageScheduler:
#     """
#     Whatsapp Web message scheduler. handles sending messages to contacts at certain times.
#     """
#
#     def __init__(self):
#         self.__scheduler = BackgroundScheduler()
#
#
#
#     def shutdown(self):
#         """
#         Shutting down the scheduler, discarding all scheduled jobs.
#         """
#         self.__scheduler.shutdown(wait=False)
#         print('Shutdown the scheduler successfully')
#
#     def __del__(self):
#         self.shutdown()

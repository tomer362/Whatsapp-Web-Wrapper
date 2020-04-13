import time
from functools import wraps

WAIT_FOR_SEARCH_TIMEOUT = 5
WAIT_FOR_SEARCH_TIME = 0.1


class Contact:
    """
    Class represents an entity that can be interacted by chat,
    it can be a group or a private chat
    """

    class ContactDecorators:
        @staticmethod
        def navigate_decorator(method):
            """
            In order to send or recive messages to contact, you must first navigate to the contact,
            using WhatsappWeb.navigate_to_contact_chat method.

            this decorator used to navigate to speocific contact, before initial the above actions
            """

            # TODO: support return to previous contact
            @wraps(method)
            def navigate_wrapper(self, *args, **kwargs):
                self.navigate_to_contact()
                return method(self, *args, **kwargs)

            return navigate_wrapper

        @staticmethod
        def lock_decorator(method):
            @wraps(method)
            def lock_wrapper(self, *args, **kwargs):
                with self.whatsapp_obj.web_lock:
                    method_result = method(self, *args, **kwargs)

                return method_result

            return lock_wrapper

    def __init__(self, name, whatsapp_obj):
        """
        Initializes Contact object.
        @param name: Contact's name
        @type name: C{str}
        @param whatsapp_obj:
        @type whatsapp_obj: whatsapp_web_wrapper.WhatsappWeb
        """

        self.name = name
        self.whatsapp_obj = whatsapp_obj
        self.web_driver = whatsapp_obj.web_driver

    def wait_for_search(self):
        should_wait = True
        total_time_waited = 0

        # Should wait until the looping icon disappeares from the search bar or if timeout occurs
        while should_wait and total_time_waited < WAIT_FOR_SEARCH_TIMEOUT:
            search_result_child_elems = self.web_driver.find_elements_by_xpath(
                "//div[@id='side']/div/div/span/button")
            if len(search_result_child_elems) > 0:
                if search_result_child_elems[0].tag_name == 'button':
                    should_wait = False

            if should_wait:
                time.sleep(WAIT_FOR_SEARCH_TIME)
                total_time_waited += WAIT_FOR_SEARCH_TIME

    def navigate_to_contact(self):
        """
        Click's on the first contact that matches the contact name. waits between every interaction for safety.
        """

        # Find the contact search bar so we can focus on it by clicking.
        contact_search_bar = self.web_driver.find_elements_by_xpath(
            "//div[@id='side']//div[contains(@class, 'copyable-text selectable-text')]")[0]
        contact_search_bar.click()

        # Type the contact's name in the search bar
        contact_search_bar.send_keys(self.name)

        # Wait for the search to work for sure
        self.wait_for_search()

        # Whatsapp randomizes the order of the divs in the panel of contacts so we need to get the order by location
        # in y axis
        contact_elements = self.web_driver.find_elements_by_xpath(
            "//div[@id='side']//div[@id='pane-side']/div/div/div/div")
        contact_elems_sorted_by_y_loc = sorted(contact_elements, key=lambda elem: elem.location['y'])
        if len(contact_elems_sorted_by_y_loc) > 0:
            contact_elems_sorted_by_y_loc[1].click()

            # Waits for contact chat to open.
            time.sleep(0.5)
            return True
        else:
            return False

    @ContactDecorators.lock_decorator
    @ContactDecorators.navigate_decorator
    def send_message(self, message):
        """
        Sends a message to this contact.
        @param message: Chat message. can be text or media.
        @type message: C{str}
        """
        chat_text_box_elem = self.web_driver.find_element_by_xpath(
            "//div[@id='main']//div[contains(@class, 'copyable-text selectable-text')]"
        )
        chat_text_box_elem.click()
        chat_text_box_elem.send_keys(message)

        # Wait for send button to be created
        time.sleep(0.4)

        # Find the send button and click it (by finding the send icon first and then going up to the button)
        send_button_elem = self.web_driver.find_element_by_xpath(
            "//div[@id='main']//footer//span[@data-icon='send']/..")
        send_button_elem.click()

    @ContactDecorators.navigate_decorator
    def receive_message(self, message):
        # TODO - recive withoud actually reading the message
        pass

    @ContactDecorators.navigate_decorator
    def get_members(self):
        pass


class Message:

    def __init__(self, text, media=None):
        self.text = text
        self.media = media

    def convert_to_msg(self):
        """
        run operations nedded to convert the message from plain text to WhatappWeb format
        """
        pass

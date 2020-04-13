import time
from functools import wraps


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
        # TODO: make it smart by searching for the search looping icon and if it disappeares it mean the search ended
        #  (or some other form of ending of search).
        time.sleep(1.5)

        # Whatsapp randomizes the order of the divs in the panel of contacts so we need to get the order by location
        # in y axis
        contat_elements = self.web_driver.find_elements_by_xpath(
            "//div[@id='side']//div[@id='pane-side']/div/div/div/div")
        contact_elems_sorted_by_y_loc = sorted(contat_elements, key=lambda x: x.location['y'])
        contact_elems_sorted_by_y_loc[1].click()

        # Waits for contact chat to open.
        time.sleep(1.5)

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

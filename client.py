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
            # ToDo: support return to prvious contact
            @wraps(method)
            def navigate_wrapper(self, *args, **kwargs):
                self.navigat_to_contact(self.name, self.whatsapp_obj)
                return method(self, *args, **kwargs)
            return navigate_wrapper


    def __init__(self, name, whatsapp_obj):
        self.name = name
        self.whatsapp_obj = whatsapp_obj


    def navigat_to_contact(self, name, whatsapp_obj):
        whatsapp_obj.navigate_to_contact_chat(name)

    
    @ContactDecorators.navigate_decorator
    def send_message(self, message):
        self.whatsapp_obj.send_message(message=message, contact_name=self.name, should_navigate_first=False)

    @ContactDecorators.navigate_decorator
    def recive_message(self, message):
        # Todo - recive withoud actually reading the message
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
# *-* coding: utf-8 *-*

from whatsapp_web_wrapper import WhatsappWebWrapper


def main():
    with WhatsappWebWrapper() as whatsapp_web:
        input("Connect With your phone and then click enter..")
        whatsapp_web.send_message('אני', 'בדיקה בדיקה', should_navigate_first=True)


if __name__ == '__main__':
    main()

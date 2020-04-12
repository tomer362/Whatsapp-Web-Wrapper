# *-* coding: utf-8 *-*

from whatsapp_web_wrapper import WhatsappWeb


def main():
    with WhatsappWeb() as whatsapp_web:
        whatsapp_web.send_message('אני', 'בדיקה בדיקה', should_navigate_first=True)


if __name__ == '__main__':
    main()

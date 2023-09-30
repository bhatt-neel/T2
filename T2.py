import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AppConfig.settings')
django.setup()
from telegram.ext import *
from Telegram.handlers import *


if __name__ == '__main__':

    TELEGRAM_BOT_API = get_config_obj().TelegramToken

    updater = Updater(TELEGRAM_BOT_API, use_context=True)

    dp = updater.dispatcher

    if get_bot_status():
        dp.add_handler(MessageHandler(Filters.text, message_handler))
        dp.add_handler(MessageHandler(Filters.photo, photo_handler))

    
    dp.add_handler(CommandHandler('status', status_handler))
    dp.add_handler(CommandHandler('fund', fund_handler))


    updater.start_polling()
    print("Bot is ready to use!")
    updater.idle()

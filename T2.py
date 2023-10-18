import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AppConfig.settings')
django.setup()
from telegram.ext import *
from Telegram.handlers import *
from Telegram.restarts import *

if __name__ == '__main__':

    if not is_token_map_updated():
        print("Updating Token Map...")
        UpdateTokenMap()

    TELEGRAM_BOT_API = get_config_obj().TelegramToken

    updater = Updater(TELEGRAM_BOT_API, use_context=True)

    def msg(update, context):
        update.message.reply_text("Please use the commands to interact with the bot.")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_handler))
    dp.add_handler(CommandHandler('stop', stop_handler))
    dp.add_handler(CommandHandler('status', status_handler))
    dp.add_handler(CommandHandler('fund', fund_handler))
    dp.add_handler(CommandHandler('token', tokenmap_handler))
    dp.add_handler(CommandHandler('restart', restart_handler))

    dp.add_handler(MessageHandler(Filters.text, message_handler))
    dp.add_handler(MessageHandler(Filters.photo, photo_handler))

    updater.start_polling()
    print("Bot is ready to use!")
    updater.idle()

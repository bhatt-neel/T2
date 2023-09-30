from App.DataHub import *
from restarts import *
from telegram import ParseMode

def message_handler(update, context):
    if get_bot_status():
        update.message.reply_text("This is a message handler")


def photo_handler(update, context):
    if get_bot_status():
        update.message.reply_text("This is a photo handler")


def status_handler(update, context):
    if get_bot_status():
        update.message.reply_text("**Bot Status:** Online\nTo stop it, please use the command `/stop`.")
    else:
        update.message.reply_text("**Bot Status:** Offline\nTo start it, please use the command `/start`.")


def fund_handler(update, context):
    Normal = str(get_config_obj().NormalBalance)
    Hero_Zero = str(get_config_obj().HeroZeroBalance)
    update.message.reply_text(f"BALANCE INFO\n\nNORMAL : {Normal}\nHERO-ZERO : {Hero_Zero}")


def tokenmap_handler(update, context):
    if is_token_map_updated():
        update.message.reply_text("Token Map is Updated!!")
    else:
        update.message.reply_text("Token Map is not Updated")

def restart_handler(update, context):
    if UpdateTokenMap():
        update.message.reply_text("Token Map Updated Successfully !!")
    else:
        update.message.reply_text("Error While Updating Token Map")

def start_handler(update, context):
    if get_bot_status():
        update.message.reply_text("Bot is Already Online\nTo stop it, please use the command `/stop`.")
    else:
        update.message.reply_text("**Bot Status:** Online\nThe bot has been initiated! To stop it, please use the command `/stop`.",
                              parse_mode=ParseMode.MARKDOWN)
        
def stop_handler(update, context):
    if not get_bot_status():
        update.message.reply_text("Bot is Already Offline\nTo start it, please use the command `/start`.")
    else:
        update.message.reply_text("**Bot Status:** Offline\nThe bot has been Shutdown! To start it, please use the command `/start`.",
                              parse_mode=ParseMode.MARKDOWN)
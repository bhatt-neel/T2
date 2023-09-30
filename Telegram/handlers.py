from App.DataHub import *

def message_handler(update, context):
    pass

def photo_handler(update, context):
    pass

def status_handler(update, context):
    if get_bot_status():
        update.message.reply_text("Offline")
    else:
        update.message.reply_text("Offline")

def fund_handler(update, context):
    Normal = str(get_config_obj().NormalBalance)
    Hero_Zero = str(get_config_obj().HeroZeroBalance)
    update.message.reply_text(f"BALANCE INFO\n\nNORMAL : {Normal}\nHERO-ZERO : {Hero_Zero}")
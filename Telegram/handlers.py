from App.DataHub import *
from Telegram.restarts import *
from telegram import ParseMode
from Logic.Parser.img_to_txt import img_to_text
from Logic.Parser.txt_to_info import text_to_info
from Logic.Parser.info_to_orderParm import Info_To_Order
from Logic.AngelOne.helper import DecideStrategy
import os
import traceback


def message_handler(update, context):  
    try:
        if get_bot_status():
            print(f"\n=================== CP1 {datetime.datetime.now()} CP1 ===================\n")
            
            print("MESSAGE ARRIVED")
            RawText = update.message.text
            print(f"MESSAGE FROM USER:\n{RawText}")

            print(f"\n=================== CP2 {datetime.datetime.now()} CP2 ===================\n")
            
            print("CONVERTING TEXT TO INFO")
            TextToInfo = text_to_info(RawText)

            print(f"\n=================== CP3 {datetime.datetime.now()} CP3 ===================\n")

            print("CONVERTING INFO TO ORDER PARM")
            JsonOrderParm = Info_To_Order(TextToInfo)

            print(f"\n=================== CP4 {datetime.datetime.now()} CP4 ===================\n")

            DecideStrategy(JsonOrderParm, update)

        return True
    
    except Exception as e:
        print(f'ERROR MESSAGE FROM MESSAGE HANDLER :\n{e}')
        traceback.print_tb(e.__traceback__)
        return False

def photo_handler(update, context):
    try:
        if get_bot_status():

            print(f"\n=================== CP1 {datetime.datetime.now()} CP1 ===================\n")
            FolderPath = os.getcwd() + "/static/TokenMapCsv/"
            FilePath = f"{FolderPath}output_image.jpg"
            file = context.bot.get_file(update.message.photo[-1].file_id)
            file.download(FilePath)
            print(f"\n=================== CP2 {datetime.datetime.now()} CP2 ===================\n")


            txtFromImg = img_to_text(FilePath)
            print(f'MESSAGE FROM IMG_TO_TEXT RESULT : \n\t\t{txtFromImg}')
            print(f"\n=================== CP3 {datetime.datetime.now()} CP3 ===================\n")


            TextToInfo = text_to_info(txtFromImg)
            print(f'\tMESSAGE FROM TXT_TO_INFO RESULT : \n\t\t{TextToInfo}')
            print(f"\n=================== CP4 {datetime.datetime.now()} CP4 ===================\n")


            JsonOrderParm = Info_To_Order(TextToInfo)
            print(f'\tMESSAGE FROM INFO_TO_ORDER RESULT : \n\t\t{JsonOrderParm}')
            print(f"\n=================== CP5 {datetime.datetime.now()} CP5 ===================\n")

            DecideStrategy(JsonOrderParm, update)

        return True
    
    except Exception as e:
        print(f'MESSAGE FROM PHOTO_HANDLER RESULT : \n{e}')
        traceback.print_tb(e.__traceback__)
        return False

def status_handler(update, context):
    if get_bot_status():
        update.message.reply_text("**Bot Status:** Online\nTo stop it, please use the command `/stop`.", parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("**Bot Status:** Offline\nTo start it, please use the command `/start`.", parse_mode=ParseMode.MARKDOWN)

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
    update.message.reply_text("Restarting Bot...")
    
    ConfigObj = get_config_obj()
    ConfigObj.BotStatus = True
    ConfigObj.save()

    if is_token_map_updated():
        update.message.reply_text("Token Map is Updated!!")
        update.message.reply_text("Bot Restarted Successfully !!")
        update.message.reply_text("**Bot Status:** Online\nThe bot has been initiated! To stop it, please use the command `/stop`.",
                              parse_mode=ParseMode.MARKDOWN)

    else:
        result = UpdateTokenMap()
        if result:
            update.message.reply_text("Token Map Updated Successfully !!")
            update.message.reply_text("Bot Restarted Successfully !!")
            update.message.reply_text("**Bot Status:** Online\nThe bot has been initiated! To stop it, please use the command `/stop`.",
                                parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text("Error While Updating Token Map")

def start_handler(update, context):
    if get_bot_status():
        update.message.reply_text("Bot is Already Online\nTo stop it, please use the command `/stop`.", parse_mode=ParseMode.MARKDOWN)
    else:
        configInfo = get_config_obj()
        configInfo.BotStatus = True
        configInfo.save()
        update.message.reply_text("**Bot Status:** Online\nThe bot has been initiated! To stop it, please use the command `/stop`.",
                              parse_mode=ParseMode.MARKDOWN)
        
def stop_handler(update, context):
    if not get_bot_status():
        update.message.reply_text("Bot is Already Offline\nTo start it, please use the command `/start`.", parse_mode=ParseMode.MARKDOWN)
    else:
        configInfo = get_config_obj()
        configInfo.BotStatus = False
        configInfo.save()
        update.message.reply_text("**Bot Status:** Offline\nThe bot has been Shutdown! To start it, please use the command `/start`.",
                              parse_mode=ParseMode.MARKDOWN)
        

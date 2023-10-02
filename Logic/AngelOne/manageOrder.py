import math
from .place_order import place_order
from .GetLtp import getLTP
from telegram import ParseMode
from App.DataHub import *
from App.models import LiveDb
import time
import pytz


def DECIDE_SL_AND_BREAK_EVEN(StrategyCode, BUYINGPRICE):
    if StrategyCode == 'SLTGT':
        StrategyConfig = get_strategy_by_code('SLTGT')
        SL = BUYINGPRICE*(1 - (StrategyConfig.SL/100))
        TGT_OR_BREAK_EVEN = BUYINGPRICE*(1 + (StrategyConfig.SL/100))
        return [True, SL, TGT_OR_BREAK_EVEN, 0]
    
    elif StrategyCode == 'TSLAP':
        StrategyConfig = get_strategy_by_code('TSLAP')
        SL = BUYINGPRICE*(1 - (StrategyConfig.SL/100))
        TGT_OR_BREAK_EVEN = BUYINGPRICE*(1 + (StrategyConfig.TrailingStartAt/100))
        TrailingMargin = 1 - (StrategyConfig.TrailingMargin/100)
        return [True, SL, TGT_OR_BREAK_EVEN, TrailingMargin]
    
    elif StrategyCode == 'TSLAPB':
        StrategyConfig = get_strategy_by_code('TSLAPB')
        SL = BUYINGPRICE*(1 - (StrategyConfig.SL/100))
        TGT_OR_BREAK_EVEN = BUYINGPRICE*(1 + (StrategyConfig.TrailingStartAt/100))
        TrailingMargin = 1 - (StrategyConfig.TrailingMargin/100)
        return [True, SL, TGT_OR_BREAK_EVEN, TrailingMargin]
    
    elif StrategyCode == 'HEROZERO':
        StrategyConfig = get_strategy_by_code('HEROZERO')
        SL = BUYINGPRICE*(1 - (StrategyConfig.SL/100))
        TGT_OR_BREAK_EVEN = BUYINGPRICE*(1 + (StrategyConfig.TrailingStartAt/100))
        TrailingMargin = 1 - (StrategyConfig.TrailingMargin/100)
        return [True, SL, TGT_OR_BREAK_EVEN, TrailingMargin]

    else:
        return [False, 0, 0, 0]

def UpdateLiveDb(BUYINGPRICE, StrategyCode, TOTAL_LOT, LOTSIZE, LTP):
    LiveDbObj = LiveDb.objects.all().first()
    Qty = TOTAL_LOT*LOTSIZE
    LiveDbObj.Strategy = StrategyCode
    LiveDbObj.BUYINGPRICE = BUYINGPRICE
    LiveDbObj.LTP = LTP
    LiveDbObj.Returns = round(((LTP - BUYINGPRICE)/BUYINGPRICE*100), 2)
    LiveDbObj.PNL = (LTP - BUYINGPRICE)*Qty
    LiveDbObj.running = True
    LiveDbObj.save()
    return True
    
def ManageForcedExit(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, update):

    try:
        ConfigObj = get_config_obj()
        FourcedExitWithoutSelling = ConfigObj.ForcedExitWithoutSelling
        FourcedExitWithSelling = ConfigObj.ForcedExitWithSelling
        
        if FourcedExitWithoutSelling:
            print(f'Forced Exit Without Selling')
            update.message.reply_text(f'Forced Exit Without Selling Remaining all QTY')
            ConfigObj.ForcedExitWithoutSelling = False
            ConfigObj.save()
            return True

        elif FourcedExitWithSelling:
            print(f'Forced Exit With Selling')
            result = place_order(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'SELL')
            update.message.reply_text(f'Forced Exit With Selling Remaining all QTY')
            ConfigObj.ForcedExitWithSelling = False
            ConfigObj.save()
            return True
        else:
            pass

    except Exception as e:
        print(f'Error in ManageForcedExit : {e}')
        return False

def ManageSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, StrategyCode, BUYINGPRICE, update):
        
    result = {}
            
    while True:

        time.sleep(0.2)

        ForcedExit = ManageForcedExit(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, update)

        if ForcedExit:
            result['CarryForward'] = False
            break
            
        STATUS, SL, BreakAt, Margin = DECIDE_SL_AND_BREAK_EVEN(StrategyCode, BUYINGPRICE)
    
        LTP = getLTP(TOKEN, SYMBOL)
    
        if LTP <= SL or LTP >=BreakAt:
                
            if LTP <= SL:
                order = place_order(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'SELL')
                result['order'] = order
                result['CarryForward'] = False
                print(f"100% QTY BOOKED WITH SL.")
                break

            elif LTP >=BreakAt:
                result['CarryForward'] = True
                print(f"BREAK EVEN POINT REACHED")
                break

        UpdateLiveDb(BUYINGPRICE, StrategyCode, TOTAL_LOT, LOTSIZE, LTP)
    
    return result

def ManageTSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, StrategyCode, BUYINGPRICE, update):
    result = {}

    HighestLTP = BUYINGPRICE
            
    while True:

        time.sleep(0.2)

        ForcedExit = ManageForcedExit(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, update)

        if ForcedExit:
            result['CarryForward'] = False
            break
            
        LTP = getLTP(TOKEN, SYMBOL)

        if HighestLTP < LTP:
            HighestLTP = LTP

        TrailingMargin = DECIDE_SL_AND_BREAK_EVEN(StrategyCode, BUYINGPRICE)[3]

        TrailingSL = HighestLTP*TrailingMargin

        if LTP <= TrailingSL:
            order = place_order(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'SELL')
            result['order'] = order
            result['CarryForward'] = True
            break

        UpdateLiveDb(BUYINGPRICE, StrategyCode, TOTAL_LOT, LOTSIZE, LTP)
    
    return result

def ManageBUY(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, StrategyCode, update):

    BUY = place_order(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'BUY')
    
    message_date = update.message.date
    ist_timezone = pytz.timezone('Asia/Kolkata')
    message_date = message_date.astimezone(ist_timezone)

    print(f"{StrategyCode} : BUYING ORDER PLACED")

    StrategyConfig = get_strategy_by_code(StrategyCode)
    SLP = StrategyConfig.SL
    TGT = StrategyConfig.TGT
    TTGT = StrategyConfig.TrailingStartAt

    status, sl, tgt, margin = DECIDE_SL_AND_BREAK_EVEN(StrategyCode, BUY['TriggerPrice'])

    if StrategyCode == 'SLTGT':
        update.message.reply_text(f"*ORDER PLACED !!*\n\n*Order :* {BUY['Symbol']}\n*Message Arrived at :* {message_date}\n*ApiExecuted at :* {str(BUY['TriggerTime'])}\n\n*SL{SLP} : * {round(sl, 2)}\n*Avg Buying Price : * {BUY['TriggerPrice']}\n*TGT{TGT} : * {round(tgt, 2)}", parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text(f"*ORDER PLACED !!*\n\n*Order :* {BUY['Symbol']}\n*Message Arrived at :* {message_date}\n*ApiExecuted at :* {str(BUY['TriggerTime'])}\n\n*SL{SLP} : * {round(sl, 2)}\n*Avg Buying Price : * {BUY['TriggerPrice']}\n*BreakEvenAt{TTGT} : * {round(tgt, 2)}", parse_mode=ParseMode.MARKDOWN)

    ConfigObj = get_config_obj()
    ConfigObj.BotStatus = False
    ConfigObj.save()
    update.message.reply_text("Bot Status: Offline\nTo activate the bot, please use the command /start.")

    return BUY
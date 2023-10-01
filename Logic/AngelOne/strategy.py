import math
from .place_order import place_order
from App.DataHub import *
from .manageOrder import ManageSL, ManageTSL, ManageBUY


def SLTGT(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, update):
    
    # Trail Stop Loss After Profit

    BUY = ManageBUY(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'SLTGT', update)

    if BUY['status']:
        BUYINGPRICE = BUY['TriggerPrice']
        Result = ManageSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'SLTGT', BUYINGPRICE, update)

        StrategyConfig = get_strategy_by_code('SLTGT')
        
        if Result['CarryForward']:
            order = place_order(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'SELL')
            print(f"SLTGT : 100% QTY BOOKED WITH TGT OF {StrategyConfig.TGT}%.")
            update.message.reply_text(f"SLTGT : 100% QTY BOOKED WITH TGT OF {StrategyConfig.TGT}%.")
        else:
            print(f"SLTGT : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
            update.message.reply_text(f"SLTGT : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
    else:
        print("SLTGT : Error While Buying Order.")
        update.message.reply_text("SLTGT : Error While Buying Order.")

    return True


def TSLAP(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, update):
    # Trail Stop Loss After Profit

    BUY = ManageBUY(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLAP', update)

    if BUY['status']:
        BUYINGPRICE = BUY['TriggerPrice']

        MSL = ManageSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLAP', BUYINGPRICE, update)
        
        StrategyConfig = get_strategy_by_code('TSLAP')

        if MSL['CarryForward']:
            print(f"TSLAP : BREAK EVEN POINT TOUCHED NOW TRAILLING ALL QTY WITH {StrategyConfig.TrailingMargin}% OF MARGIN.")
            update.message.reply_text(f"TSLAP : BREAK EVEN POINT TOUCHED NOW TRAILLING ALL QTY WITH {StrategyConfig.TrailingMargin}% OF MARGIN.")
            TSL = ManageTSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLAP', BUYINGPRICE, update)
            print(f"TSLAP : {StrategyConfig.TrailingMargin}% OF TRAILING SL HIT.")
            update.message.reply_text(f"TSLAP : {StrategyConfig.TrailingMargin}% OF TRAILING SL HIT.")

        else:
            print(f"TSLAP : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
            update.message.reply_text(f"TSLAP : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
    else:
        print("TSLAP : Error While Buying Order.")
        update.message.reply_text("TSLAP : Error While Buying Order.")

    return True


def TSLAPB(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, update):
    # Trail Stop Loss After Profit

    BUY = ManageBUY(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLAPB', update)

    if BUY['status']:
        BUYINGPRICE = BUY['TriggerPrice']

        LOT_TGT_1 = math.ceil(TOTAL_LOT/2)
        LOT_TGT_2 = TOTAL_LOT - LOT_TGT_1

        MSL = ManageSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLAPB', BUYINGPRICE, update)
        
        StrategyConfig = get_strategy_by_code('TSLAPB')

        if MSL['CarryForward']:
            order = place_order(TOKEN, SYMBOL, LOT_TGT_1, LOTSIZE, 'SELL')
            print(f"TSLAPB : 50% QTY BOOKED AT {StrategyConfig.TrailingStartAt}% OF TGT.")
            update.message.reply_text(f"TSLAPB : 50% QTY BOOKED AT {StrategyConfig.TrailingStartAt}% OF TGT.")
            TSL = ManageTSL(TOKEN, SYMBOL, LOT_TGT_2, LOTSIZE, 'TSLAPB', BUYINGPRICE, update)
            print(f"TSLAPB : {StrategyConfig.TrailingMargin}% MARGIN OF TRAILING SL HIT.")
            update.message.reply_text(f"TSLAPB : {StrategyConfig.TrailingMargin}% MARGIN OF TRAILING SL HIT.")

        else:
            print(f"TSLAPB : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
            update.message.reply_text(f"TSLAPB : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
    
    else:
        print("TSLAPB : Error While Buying Order.")
        update.message.reply_text("TSLAPB : Error While Buying Order.")

    return True


def HEROZERO(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, update):
    # HERO ZERO
    
    BUY = ManageBUY(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'HEROZERO', update)

    if BUY['status']:
        BUYINGPRICE = BUY['TriggerPrice']    

        MSL = ManageSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'HEROZERO', BUYINGPRICE, update)
        
        StrategyConfig = get_strategy_by_code('HEROZERO')

        if MSL['CarryForward']:
            print(f"HEROZERO : BREAK EVEN POINT TOUCHED NOW TRAILLING ALL QTY WITH {StrategyConfig.TrailingMargin}% OF MARGIN.")
            update.message.reply_text(f"HEROZERO : BREAK EVEN POINT TOUCHED NOW TRAILLING ALL QTY WITH {StrategyConfig.TrailingMargin}% OF MARGIN.")
            TSL = ManageTSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'HEROZERO', BUYINGPRICE, update)
            print(f"HEROZERO : {StrategyConfig.TrailingMargin}% OF TRAILING SL HIT.")
            update.message.reply_text(f"HEROZERO : {StrategyConfig.TrailingMargin}% OF TRAILING SL HIT.")

        else:
            print(f"HEROZERO : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
            update.message.reply_text(f"HEROZERO : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")

    else:
        print("HEROZERO : Error While Buying Order.")
        update.message.reply_text("HEROZERO : Error While Buying Order.")

    return True
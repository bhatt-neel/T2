import math
from .place_order import place_order
from App.DataHub import *
from .manageOrder import ManageSL, ManageTSL, ManageBUY, ManageTslOnProfit
from App.models import Transaction, Order, LiveDb


def SLTGT(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, EXCHANGE, update):
    
    # Trail Stop Loss After Profit

    BUY = ManageBUY(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'SLTGT', EXCHANGE, update)

    if BUY['status']:
        orderObj = Order(
            OrderSymbol=SYMBOL,
            OrderStatus=False,
            StrategyCode='SLTGT'
        )
        orderObj.save()
        BuyObj = Transaction(
            OrderObj=orderObj,
            TransactionSymbol=SYMBOL,
            BuySell='BUY',
            TransactionLotSize=TOTAL_LOT,
            TransactionLot=TOTAL_LOT,
            TriggerPrice=BUY['TriggerPrice'],
            status=True
        )
        BuyObj.save()

        BUYINGPRICE = BUY['TriggerPrice']
        Result = ManageSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'SLTGT', BUYINGPRICE, EXCHANGE, update)

        StrategyConfig = get_strategy_by_code('SLTGT')
        
        if Result['CarryForward']:
            order = place_order(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'SELL', EXCHANGE)

            SellObj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=TOTAL_LOT,
                TransactionLot=TOTAL_LOT,
                TriggerPrice=order['TriggerPrice'],
                status=True
            )
            SellObj.save()
            orderObj.OrderStatus = True
            orderObj.save()

            LiveDbObj = LiveDb.objects.all().first()
            LiveDbObj.running = False
            LiveDbObj.save()

            print(f"SLTGT : 100% QTY BOOKED WITH TGT OF {StrategyConfig.TGT}%.")
            update.message.reply_text(f"SLTGT : 100% QTY BOOKED WITH TGT OF {StrategyConfig.TGT}%.")
        else:
            SellObj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=TOTAL_LOT,
                TransactionLot=TOTAL_LOT,
                TriggerPrice=Result['order']['TriggerPrice'],
                status=True
            )
            SellObj.save()
            orderObj.OrderStatus = True
            orderObj.save()
            LiveDbObj = LiveDb.objects.all().first()
            LiveDbObj.running = False
            LiveDbObj.save()
            print(f"SLTGT : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
            update.message.reply_text(f"SLTGT : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
    else:
        print("SLTGT : Error While Buying Order.")
        update.message.reply_text("SLTGT : Error While Buying Order.")

    return True


def TSLAP(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, EXCHANGE, update):
    # Trail Stop Loss After Profit

    BUY = ManageBUY(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLAP', EXCHANGE, update)

    if BUY['status']:
        orderObj = Order(
            OrderSymbol=SYMBOL,
            OrderStatus=False,
            StrategyCode='SLTGT'
        )
        orderObj.save()
        BuyObj = Transaction(
            OrderObj=orderObj,
            TransactionSymbol=SYMBOL,
            BuySell='BUY',
            TransactionLotSize=LOTSIZE,
            TransactionLot=TOTAL_LOT,
            TriggerPrice=BUY['TriggerPrice'],
            status=True
        )
        BuyObj.save()
        BUYINGPRICE = BUY['TriggerPrice']

        MSL = ManageSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLAP', BUYINGPRICE, EXCHANGE, update)
        
        StrategyConfig = get_strategy_by_code('TSLAP')

        if MSL['CarryForward']:
            print(f"TSLAP : BREAK EVEN POINT TOUCHED NOW TRAILLING ALL QTY WITH {StrategyConfig.TrailingMargin}% OF MARGIN.")
            update.message.reply_text(f"TSLAP : BREAK EVEN POINT TOUCHED NOW TRAILLING ALL QTY WITH {StrategyConfig.TrailingMargin}% OF MARGIN.")
            TSL = ManageTSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLAP', BUYINGPRICE, EXCHANGE, update)
            SellObj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=LOTSIZE,
                TransactionLot=TOTAL_LOT,
                TriggerPrice=TSL['order']['TriggerPrice'],
                status=True
            )
            SellObj.save()
            orderObj.OrderStatus = True
            orderObj.save()
            LiveDbObj = LiveDb.objects.all().first()
            LiveDbObj.running = False
            LiveDbObj.save()
            print(f"TSLAP : {StrategyConfig.TrailingMargin}% OF TRAILING SL HIT.")
            update.message.reply_text(f"TSLAP : {StrategyConfig.TrailingMargin}% OF TRAILING SL HIT.")

        else:
            SellObj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=LOTSIZE,
                TransactionLot=TOTAL_LOT,
                TriggerPrice=MSL['order']['TriggerPrice'],
                status=True
            )
            SellObj.save()
            orderObj.OrderStatus = True
            orderObj.save()
            LiveDbObj = LiveDb.objects.all().first()
            LiveDbObj.running = False
            LiveDbObj.save()
            print(f"TSLAP : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
            update.message.reply_text(f"TSLAP : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
    else:
        print("TSLAP : Error While Buying Order.")
        update.message.reply_text("TSLAP : Error While Buying Order.")

    return True


def TSLOP(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, EXCHANGE, update):
    # Trail Stop Loss On Profit

    BUY = ManageBUY(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLOP', EXCHANGE, update)

    if BUY['status']:
        orderObj = Order(
            OrderSymbol=SYMBOL,
            OrderStatus=False,
            StrategyCode='TSLOP'
        )
        orderObj.save()
        BuyObj = Transaction(
            OrderObj=orderObj,
            TransactionSymbol=SYMBOL,
            BuySell='BUY',
            TransactionLotSize=LOTSIZE,
            TransactionLot=TOTAL_LOT,
            TriggerPrice=BUY['TriggerPrice'],
            status=True
        )
        BuyObj.save()
        BUYINGPRICE = BUY['TriggerPrice']

        MSL = ManageSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLOP', BUYINGPRICE, EXCHANGE, update)
        
        StrategyConfig = get_strategy_by_code('TSLOP')

        if MSL['CarryForward']:
            print(f"TSLOP : BREAK EVEN POINT TOUCHED NOW TRAILLING ALL QTY WITH {StrategyConfig.TrailingMargin}% OF MARGIN.")
            update.message.reply_text(f"TSLOP : BREAK EVEN POINT TOUCHED NOW TRAILLING ALL QTY WITH {StrategyConfig.TrailingMargin}% OF MARGIN ( ROI ).")
            TSL = ManageTslOnProfit(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLOP', BUYINGPRICE, EXCHANGE, update)
            SellObj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=LOTSIZE,
                TransactionLot=TOTAL_LOT,
                TriggerPrice=TSL['order']['TriggerPrice'],
                status=True
            )
            SellObj.save()
            orderObj.OrderStatus = True
            orderObj.save()
            LiveDbObj = LiveDb.objects.all().first()
            LiveDbObj.running = False
            LiveDbObj.save()
            print(f"TSLOP : {StrategyConfig.TrailingMargin}% OF TRAILING SL HIT.")
            update.message.reply_text(f"TSLOP : {StrategyConfig.TrailingMargin}% OF TRAILING SL HIT.")

        else:
            SellObj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=LOTSIZE,
                TransactionLot=TOTAL_LOT,
                TriggerPrice=MSL['order']['TriggerPrice'],
                status=True
            )
            SellObj.save()
            orderObj.OrderStatus = True
            orderObj.save()
            LiveDbObj = LiveDb.objects.all().first()
            LiveDbObj.running = False
            LiveDbObj.save()
            print(f"TSLOP : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
            update.message.reply_text(f"TSLAP : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
    else:
        print("TSLOP : Error While Buying Order.")
        update.message.reply_text("TSLOP : Error While Buying Order.")

    return True


def TSLAPB(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, EXCHANGE, update):
    # Trail Stop Loss After Profit

    BUY = ManageBUY(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLAPB', EXCHANGE, update)

    if BUY['status']:
        orderObj = Order(
            OrderSymbol=SYMBOL,
            OrderStatus=False,
            StrategyCode='SLTGT'
        )
        orderObj.save()
        BuyObj = Transaction(
            OrderObj=orderObj,
            TransactionSymbol=SYMBOL,
            BuySell='BUY',
            TransactionLotSize=LOTSIZE,
            TransactionLot=TOTAL_LOT,
            TriggerPrice=BUY['TriggerPrice'],
            status=True
        )
        BuyObj.save()
        BUYINGPRICE = BUY['TriggerPrice']

        LOT_TGT_1 = math.ceil(TOTAL_LOT*0.70)
        LOT_TGT_2 = TOTAL_LOT - LOT_TGT_1

        MSL = ManageSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'TSLAPB', BUYINGPRICE, EXCHANGE, update)
        
        StrategyConfig = get_strategy_by_code('TSLAPB')

        if MSL['CarryForward']:
            order = place_order(TOKEN, SYMBOL, LOT_TGT_1, LOTSIZE, 'SELL', EXCHANGE)
            Sell1Obj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=LOTSIZE,
                TransactionLot=LOT_TGT_1,
                TriggerPrice=order['TriggerPrice'],
                status=True
            )
            Sell1Obj.save()
            
            print(f"TSLAPB : 50% QTY BOOKED AT {StrategyConfig.TrailingStartAt}% OF TGT.")
            update.message.reply_text(f"TSLAPB : 50% QTY BOOKED AT {StrategyConfig.TrailingStartAt}% OF TGT.")
            TSL = ManageTSL(TOKEN, SYMBOL, LOT_TGT_2, LOTSIZE, 'TSLAPB', BUYINGPRICE, EXCHANGE, update)
            Sell2Obj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=LOTSIZE,
                TransactionLot=LOT_TGT_2,
                TriggerPrice=TSL['order']['TriggerPrice'],
                status=True
            )
            Sell2Obj.save()
            orderObj.OrderStatus = True
            orderObj.save()
            LiveDbObj = LiveDb.objects.all().first()
            LiveDbObj.running = False
            LiveDbObj.save()
            print(f"TSLAPB : {StrategyConfig.TrailingMargin}% MARGIN OF TRAILING SL HIT.")
            update.message.reply_text(f"TSLAPB : {StrategyConfig.TrailingMargin}% MARGIN OF TRAILING SL HIT.")

        else:
            SellObj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=LOTSIZE,
                TransactionLot=TOTAL_LOT,
                TriggerPrice=MSL['order']['TriggerPrice'],
                status=True
            )
            SellObj.save()
            orderObj.OrderStatus = True
            orderObj.save()
            LiveDbObj = LiveDb.objects.all().first()
            LiveDbObj.running = False
            LiveDbObj.save()
            print(f"TSLAPB : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
            update.message.reply_text(f"TSLAPB : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
    
    else:
        print("TSLAPB : Error While Buying Order.")
        update.message.reply_text("TSLAPB : Error While Buying Order.")

    return True


def HEROZERO(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, EXCHANGE, update):
    # HERO ZERO
    
    BUY = ManageBUY(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'HEROZERO', EXCHANGE, update)

    if BUY['status']:
        orderObj = Order(
            OrderSymbol=SYMBOL,
            OrderStatus=False,
            StrategyCode='SLTGT'
        )
        orderObj.save()
        BuyObj = Transaction(
            OrderObj=orderObj,
            TransactionSymbol=SYMBOL,
            BuySell='BUY',
            TransactionLotSize=LOTSIZE,
            TransactionLot=TOTAL_LOT,
            TriggerPrice=BUY['TriggerPrice'],
            status=True
        )
        BuyObj.save()
        BUYINGPRICE = BUY['TriggerPrice']    

        MSL = ManageSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'HEROZERO', BUYINGPRICE, EXCHANGE, update)
        
        StrategyConfig = get_strategy_by_code('HEROZERO')

        if MSL['CarryForward']:
            print(f"HEROZERO : BREAK EVEN POINT TOUCHED NOW TRAILLING ALL QTY WITH {StrategyConfig.TrailingMargin}% OF MARGIN.")
            update.message.reply_text(f"HEROZERO : BREAK EVEN POINT TOUCHED NOW TRAILLING ALL QTY WITH {StrategyConfig.TrailingMargin}% OF MARGIN.")
            TSL = ManageTSL(TOKEN, SYMBOL, TOTAL_LOT, LOTSIZE, 'HEROZERO', BUYINGPRICE, EXCHANGE, update)
            SellObj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=LOTSIZE,
                TransactionLot=TOTAL_LOT,
                TriggerPrice=TSL['order']['TriggerPrice'],
                status=True
            )
            SellObj.save()
            orderObj.OrderStatus = True
            orderObj.save()
            LiveDbObj = LiveDb.objects.all().first()
            LiveDbObj.running = False
            LiveDbObj.save()
            print(f"HEROZERO : {StrategyConfig.TrailingMargin}% OF TRAILING SL HIT.")
            update.message.reply_text(f"HEROZERO : {StrategyConfig.TrailingMargin}% OF TRAILING SL HIT.")

        else:
            SellObj = Transaction(
                OrderObj=orderObj,
                TransactionSymbol=SYMBOL,
                BuySell='SELL',
                TransactionLotSize=LOTSIZE,
                TransactionLot=TOTAL_LOT,
                TriggerPrice=MSL['order']['TriggerPrice'],
                status=True
            )
            SellObj.save()
            orderObj.OrderStatus = True
            orderObj.save()
            LiveDbObj = LiveDb.objects.all().first()
            LiveDbObj.running = False
            LiveDbObj.save()
            print(f"HEROZERO : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")
            update.message.reply_text(f"HEROZERO : 100% QTY BOOKED WITH SL OF {StrategyConfig.SL}%.")

    else:
        print("HEROZERO : Error While Buying Order.")
        update.message.reply_text("HEROZERO : Error While Buying Order.")

    return True
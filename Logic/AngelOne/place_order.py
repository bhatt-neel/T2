import traceback
import datetime
from .GetLtp import getLTP
from App.DataHub import *
from SmartApi import SmartConnect
import math

def place_order(TOKEN, SYMBOL, LOT, LOTSIZE, BUYSELL, EXCHANGE):
    
    configInfo = get_config_obj()

    obj=SmartConnect(
        api_key=configInfo.AngleOneApiKey, 
        access_token=configInfo.AngleOneAccessToken,
        refresh_token=configInfo.AngleOneRefreshToken,
        feed_token=configInfo.AngleOneFeedToken,
        userId=configInfo.AngleOneUserId
    )


    try:

        TOTAL_QTY_TO_SELL = LOT*LOTSIZE
        lags = TOTAL_QTY_TO_SELL/900
        LowerCounter = math.floor(lags)
        UpperCounter = math.ceil(lags)

        while UpperCounter > 0:

            if UpperCounter == 1:
                QTY_TO_SELL = TOTAL_QTY_TO_SELL - (900*LowerCounter)
            else:
                QTY_TO_SELL = 900
            
            UpperCounter = UpperCounter - 1

            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": SYMBOL,
                "symboltoken": TOKEN,
                "transactiontype": BUYSELL,
                "exchange": EXCHANGE,
                "ordertype": 'MARKET',
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": 0,
                "squareoff": "0",
                "stoploss": "0",
                "quantity": QTY_TO_SELL,
            }

            orderId=obj.placeOrder(orderparams)
            print(orderId)

        result = {}
        result['TriggerTime'] = datetime.datetime.now()
        result['status'] = True
        result['orderId'] = 1234
        result['TransactionType'] = BUYSELL
        result['TriggerPrice'] = getLTP(EXCHANGE, TOKEN, SYMBOL)
        result['Symbol'] = SYMBOL
        result['LOTSIZE'] = LOTSIZE
        result['LOT'] = LOT
        result['QTY'] = LOT*LOTSIZE
        result['LotPrice'] = result['LOTSIZE']*result['TriggerPrice']
        result['total_amount'] = result['QTY']*result['TriggerPrice']
        return result

    except Exception as e:
        print("this is error response")
        print(e)
        traceback.print_tb(e.__traceback__)
        result = {}
        result['status'] = False
        print('Error Occurd')
        return result
    

def fake_place_order(TOKEN, SYMBOL, LOT, LOTSIZE, BUYSELL, EXCHANGE):

    try:
        result = {}
        result['TriggerTime'] = datetime.datetime.now()
        result['status'] = True
        result['TransactionType'] = BUYSELL
        result['TriggerPrice'] = getLTP(EXCHANGE, TOKEN, SYMBOL)
        result['Symbol'] = SYMBOL
        result['LOTSIZE'] = LOTSIZE
        result['LOT'] = LOT
        result['QTY'] = LOT*LOTSIZE
        result['LotPrice'] = result['LOTSIZE']*result['TriggerPrice']
        result['total_amount'] = result['QTY']*result['TriggerPrice']
        return result

    except Exception as e:
        traceback.print_tb(e.__traceback__)
        result = {}
        result['status'] = False
        print('Error Occurd')
        return result

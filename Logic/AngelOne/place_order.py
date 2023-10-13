import traceback
import datetime
from .GetLtp import getLTP
from App.DataHub import *
from SmartApi import SmartConnect


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
            "quantity": LOT*LOTSIZE,
        }

        orderId=obj.placeOrder(orderparams)
        result = {}
        result['TriggerTime'] = datetime.datetime.now()
        result['status'] = True
        result['orderId'] = orderId
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
    

def fake_place_order(TOKEN, SYMBOL, LOT, LOTSIZE, BUYSELL, EXCHANGE):
    
    configInfo = get_config_obj()

    try:

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
            "quantity": LOT*LOTSIZE,
        }

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

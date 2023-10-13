from SmartApi import SmartConnect
from App.DataHub import get_config_obj

def getLTP(EXCHANGE, TOKEN, SYMBOL):
    configInfo = get_config_obj()

    obj=SmartConnect(
        api_key=configInfo.AngleOneApiKey, 
        access_token=configInfo.AngleOneAccessToken,
        refresh_token=configInfo.AngleOneRefreshToken,
        feed_token=configInfo.AngleOneFeedToken,
        userId=configInfo.AngleOneUserId
    )

    instrument_data = obj.ltpData(EXCHANGE, SYMBOL, TOKEN)
    ltp = instrument_data['data']['ltp']
    return ltp


# def getLTP(TOKEN, SYMBOL):
#     f = open('/Users/neel/T2/tmpLTP.txt', 'r')
#     ltp = float(f.read())
#     return ltp
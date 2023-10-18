from SmartApi import SmartConnect
from App.DataHub import get_config_obj
from App.models import LiveDb

def getLTP(EXCHANGE, TOKEN, SYMBOL):
    configInfo = get_config_obj()

    if configInfo.FakeLTPStatus:
        fakeLtp = LiveDb.objects.all().first().FakeLTP
        return fakeLtp

    else:
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
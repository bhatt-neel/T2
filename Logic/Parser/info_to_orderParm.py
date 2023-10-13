from Logic.AngelOne.helper import getTokenInfo, getAffordableLotSize, getLTP
from App.DataHub import get_config_obj

def Info_To_Order(InfoTxt):
    configObj = get_config_obj()
    CEPE_FILTERS = {'CE':'CE', 'CALL':'CE', 'ce':'CE', 'call':'CE', 'Call':'CE', 'PE':'PE', 'PUT':'PE', 'pe':'PE', 'put':'PE', 'Put':'PE'}

    INDEX = InfoTxt['index']
    SP = int(InfoTxt['strike_price'])
    CEPE = CEPE_FILTERS[InfoTxt['type']]
    ISVALID = InfoTxt['valid_message']
    TokenInfo = getTokenInfo(INDEX, CEPE, SP).iloc[0]
    print(TokenInfo)
    symbol = TokenInfo['symbol']
    token = TokenInfo['token']
    exchange = TokenInfo['exch_seg']
    lotSize = int(TokenInfo['lotsize'])
    ltp = getLTP(exchange, token, symbol)

    if ltp < 14:
        HERO_ZERO_BALANCE = configObj.HeroZeroBalance
        AffordableLots = getAffordableLotSize(exchange, token, symbol, lotSize, HERO_ZERO_BALANCE)
    else:
        WalletBalance = configObj.NormalBalance
        AffordableLots = getAffordableLotSize(exchange, token, symbol, lotSize, WalletBalance)


    OrderParm = {
        'Index':INDEX,
        'SP':SP,
        'CEPE':CEPE,
        'LotSize': lotSize,
        'LOT': AffordableLots,
        'Token':token,
        'Symbol':symbol,
        'ltp': ltp,
        'Message' : 'Message From PaLM2 API',
        'exchange':exchange,
        'isValid':ISVALID
    }

    print(f"Index:{INDEX}\nSP:{SP}\nCEPE:{CEPE}\nLotSize: {lotSize}\nLOTS TO BUY: {AffordableLots}\nLTP: {ltp}")

    return OrderParm
    
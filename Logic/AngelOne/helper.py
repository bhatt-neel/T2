from App.DataHub import *
import math
from .strategy import SLTGT, TSLAP, TSLAPB, HEROZERO
import datetime
import pandas as pd
from .GetLtp import getLTP


def RiskManagment(AffordableLot):
    if AffordableLot > 0 and AffordableLot < 10:
        return False
    elif AffordableLot >= 10:
        return True
    

def getAffordableLotSize(TOKEN, SYMBOL, LOTSIZE, WalletBalance):
    ltp = getLTP(TOKEN, SYMBOL)
    AffordableLot = math.floor(int(WalletBalance / (ltp * LOTSIZE)))
    return AffordableLot


def getTokenInfo(SYMBOL, CEPE, SP):
    exch_seg = 'NFO'
    instrumenttype = 'OPTIDX'
    FolderPath = os.getcwd() + "/static/TokenMapCsv/"
    TokenMapPath = f"{FolderPath}{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"
    df = pd.read_csv(TokenMapPath, low_memory=False)
    SP = SP*100

    if exch_seg == 'NSE':
        eq_df = df[(df['exch_seg'] == 'NSE') & (df['symbol'].str.contains('EQ')) ]
        return eq_df[eq_df['name'] == SYMBOL]
    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == SYMBOL)].sort_values(by=['expiry'])
    elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == SYMBOL) & (df['strike'] == SP) & (df['symbol'].str.endswith(CEPE))].sort_values(by=['expiry'])


def DecideStrategy(JsonOrderParm, update):
    if JsonOrderParm['isValid']:
        print("DecideStrategy : ORDER IS VALID!")
        TOKEN = JsonOrderParm['Token']
        SYMBOL = JsonOrderParm['Symbol']
        CEPE = JsonOrderParm['CEPE']
        LOT = JsonOrderParm['LOT']
        LOTSIZE = JsonOrderParm['LotSize']
        LTP = JsonOrderParm['ltp']
        ConfigObj = get_config_obj()

        print("DecideStrategy : INFORMATION EXTRACTED SUCCESSFULLY!")

        if LOT > 0 and LOT < 2:
            
            if ConfigObj.ActiveStrategyCodeFor0T1 == 'TSLAP':
                print("DecideStrategy : MOVING FORWARD WITH TSLAP")
                Strategy = TSLAP(TOKEN, SYMBOL, LOT, LOTSIZE, update)

            elif ConfigObj.ActiveStrategyCodeFor0T1 == 'SLTGT':
                print("DecideStrategy : MOVING FORWARD WITH SLTGT")
                Strategy = SLTGT(TOKEN, SYMBOL, LOT, LOTSIZE, update)
                
        
        elif LOT >= 2:

            if LTP <= 16:
                if ConfigObj.HeroZeroStatus:
                    print("DecideStrategy : MOVING FORWARD WITH SL_TEN_TGT_TRAIL_WITH_HERO_ZERO")
                    Strategy = HEROZERO(TOKEN, SYMBOL, LOT, LOTSIZE, update)
                else:
                    print("DecideStrategy : Avoiding This HeroZero No More Greediness")
                    update.message.reply_text("DecideStrategy : Avoiding This HeroZero No More Greediness")
                    Strategy = {'status': False}
            
            else:
                if ConfigObj.ActiveStrategyCodeFor0TAll == 'TSLAP':
                    print("DecideStrategy : MOVING FORWARD WITH TSLAP")
                    Strategy = TSLAP(TOKEN, SYMBOL, LOT, LOTSIZE, update)

                elif ConfigObj.ActiveStrategyCodeFor0TAll == 'TSLAPB':
                    print("DecideStrategy : MOVING FORWARD WITH TSLAPB")
                    Strategy = TSLAPB(TOKEN, SYMBOL, LOT, LOTSIZE, update)

                elif ConfigObj.ActiveStrategyCodeFor0TAll == 'SLTGT':
                    print("DecideStrategy : MOVING FORWARD WITH SLTGT")
                    Strategy = SLTGT(TOKEN, SYMBOL, LOT, LOTSIZE, update)
        else:
            print("DecideStrategy : Wallet Balance is Too Low To Buy This Order")
            update.message.reply_text("DecideStrategy : Wallet Balance is Too Low To Buy This Order")
            Strategy = {'status': False}

    return Strategy

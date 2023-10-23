from App.DataHub import *
import requests
from SmartApi import SmartConnect
import pyotp
import pandas as pd
import datetime


def UpdateTokenMap():
    try:
        url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
        d = requests.get(url).json()
        token_df = pd.DataFrame.from_dict(d)
        token_df['expiry'] = pd.to_datetime(token_df['expiry'])
        token_df = token_df.astype({'strike': float})
        FolderPath = os.getcwd() + "/static/TokenMapCsv/"
        TokenMapPath = f"{FolderPath}{datetime.datetime.now().strftime('%Y-%m-%d')}.csv"
        token_df.to_csv(TokenMapPath, index=False)

        confObj = get_config_obj()
        confObj = Configuration.objects.all().first()

        OBJ=SmartConnect(api_key=confObj.AngleOneApiKey)
        OBJ.generateSession(confObj.AngleOneUserName,confObj.AngleOnePassword, pyotp.TOTP(confObj.AngleOneTotp).now())

        confObj.AngleOneAccessToken = OBJ.access_token
        confObj.AngleOneRefreshToken = OBJ.refresh_token
        confObj.AngleOneUserId = OBJ.feed_token
        confObj.AngleOneFeedToken = OBJ.userId
        confObj.TokenUpdatedDate = datetime.datetime.now()
        confObj.save()
        print("Token Map Updated Successfully")
        return True

    except Exception as e:
        print(e)
        print("Error While Updating Token Map")
        return False

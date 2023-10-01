from .models import Strategy, Transaction, Order, Configuration
import os
import datetime

def get_strategy_by_code(StrategyCode):
    try:
        return Strategy.objects.get(StrategyCode=StrategyCode)
    
    except Strategy.DoesNotExist:
        print("Strategy Does Not Exist")
        return None
    
def get_config_obj():
    try:
        return Configuration.objects.all().first()
    
    except Configuration.DoesNotExist:
        print("Configuration Does Not Exist")
        return None
    
def get_bot_status():
    try:
        return get_config_obj().BotStatus
    except:
        return False
    
def is_token_map_updated():

    try:
        TokenMapPath = os.getcwd() + "/static/TokenMapCsv/"
        items_in_directory = os.listdir(TokenMapPath)
        files_in_directory = [item for item in items_in_directory if os.path.isfile(os.path.join(TokenMapPath, item))]
        TodaysDate = datetime.datetime.now().strftime("%Y-%m-%d")
        ExpectedFileName = TodaysDate + ".csv"

        if ExpectedFileName in files_in_directory:
            return True
        else:
            print("Token Map is not Updated")
            return False
        
    except:
        print("Error While Checking Token Map")
        return False

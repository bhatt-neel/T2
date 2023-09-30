from .models import Strategy, Transaction, Order, Configuration

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
    
    

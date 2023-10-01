from .DataHub import *
from Telegram.restarts import *
from django.contrib import messages

def restart_bot():
    ConfigObj = get_config_obj()
    ConfigObj.BotStatus = True
    ConfigObj.save()

    if is_token_map_updated():
        print("Token Map is Updated!!")
        return True
    
    else:
        result = UpdateTokenMap()
        if result:
            print("Token Map Updated Successfully !!")
            return True
        else:
            print("Error While Updating Token Map")
            return False
    

def EditConfiguration(request):
    try:
        ConfigObj = get_config_obj()

        ConfigObj.ConfigurationName = request.POST['ConfigurationName']

        ConfigObj.ActiveStrategyCodeFor0T1 = request.POST['ActiveStrategyCodeFor0T1']
        ConfigObj.ActiveStrategyCodeFor0TAll = request.POST['ActiveStrategyCodeFor0TAll']

        ConfigObj.NormalBalance = request.POST['NormalBalance']
        ConfigObj.HeroZeroBalance = request.POST['HeroZeroBalance']

        ConfigObj.save()
        messages.success(request, 'Configuration Updated Successfully !!')
        return True
    
    except Exception as e:
        messages.error(request, 'Error While Updating Configuration')
        messages.error(request, str(e))
        return False
    
def EditStrategy(request):
    try:
        strategyCode = request.POST['strategyCode']
        StrategyObj = get_strategy_by_code(strategyCode)

        TGT = request.POST['TGT']
        TrailingMargin = request.POST['TrailingMargin']
        TrailingStartAt = request.POST['TrailingStartAt']

            

        StrategyObj.StrategyName = request.POST['StrategyName']
        StrategyObj.StrategyDescription = request.POST['StrategyDescription']
        
        StrategyObj.SL = request.POST['SL']
        if TGT != 'None':
            StrategyObj.TGT = TGT
        
        if TrailingMargin != 'None':
            StrategyObj.TrailingMargin = TrailingMargin

        if TrailingStartAt != 'None':
            StrategyObj.TrailingStartAt = TrailingStartAt

        StrategyObj.save()

        messages.success(request, 'Strategy Updated Successfully !!')
        return True
    
    except Exception as e:
        messages.error(request, 'Error While Updating Strategy')
        messages.error(request, str(e))
        return False
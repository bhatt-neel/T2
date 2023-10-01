from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .DataHub import *
from .FrontLogic import *
from django.contrib import messages


@method_decorator(login_required(login_url='admin/login/?next=/'), name='dispatch')
class IndexPage(View):
    def get(self, request):
        data = {}
        data['BotStatus'] = get_bot_status()
        data['ConfObj'] = get_config_obj()
        data['TokenStatus'] = is_token_map_updated()
        data['Strategy'] = Strategy.objects.all()
        return render(request, 'Pages/index.html', data)
    
    def post(self, request):

        if request.POST['Configuration'] == '1':
            result = EditConfiguration(request)

        elif request.POST['Configuration'] == '2':
            result = EditStrategy(request)

        return redirect('homepage')

    

def restartBot(request):
    result = restart_bot()
    if result:
        messages.success(request, 'Bot Restarted Successfully !!')
    else:
        messages.error(request, 'Error While Restarting Bot')
    return redirect('homepage')


def startBot(request):
    try:
        ConfigObj = get_config_obj()
        ConfigObj.BotStatus = True
        ConfigObj.save()
        messages.success(request, 'Bot Started Successfully !!')
    
    except Exception as e:
        messages.error(request, 'Error While Starting Bot')

    return redirect('homepage')


def stopBot(request):
    try:
        ConfigObj = get_config_obj()
        ConfigObj.BotStatus = False
        ConfigObj.save()
        messages.success(request, 'Bot Stopped Successfully !!')
    
    except Exception as e:
        messages.error(request, 'Error While Stopping Bot')

    return redirect('homepage')


def hzStart(request):
    try:
        ConfigObj = get_config_obj()
        ConfigObj.HeroZeroStatus = True
        ConfigObj.save()
        messages.success(request, 'Hero Zero Started Successfully !!')
    
    except Exception as e:
        messages.error(request, 'Error While Starting Hero Zero')

    return redirect('homepage')


def hzStop(request):
    try:
        ConfigObj = get_config_obj()
        ConfigObj.HeroZeroStatus = False
        ConfigObj.save()
        messages.success(request, 'Hero Zero Stopped Successfully !!')
    
    except Exception as e:
        messages.error(request, 'Error While Stopping Hero Zero')

    return redirect('homepage')


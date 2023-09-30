from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import telegram
from django.conf import settings


# @method_decorator(login_required(login_url='admin/'), name='dispatch')
class IndexPage(View):
    def get(self, request):
        data = {}
        return render(request, 'Pages/index.html', data)


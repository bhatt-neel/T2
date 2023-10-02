from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexPage.as_view(), name="homepage"),
    path('restartBot/', restartBot, name="restartBot"),
    path('startBot/', startBot, name="startBot"),
    path('stopBot/', stopBot, name="stopBot"),
    path('hz-start/', hzStart, name="hzStart"),
    path('hz-stop/', hzStop, name="hzStart"),
    path('edit-configuration/', EditConfiguration, name="EditConfiguration"),
    path('f-exit-and-sell/', ExitAndSell, name="EXITANDSELL"),
    path('f-exit/', Exit, name="EXIT"),
    path('ideal/', IDEAL, name="IDEAL"),
    path('api/fetch_orders/', fetch_orders, name='fetch_orders'),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


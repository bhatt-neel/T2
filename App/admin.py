from django.contrib import admin
from .models import Configuration, Order, Transaction, Strategy, LiveDb

# Register your models here.

admin.site.register(Configuration)
admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(Strategy)
admin.site.register(LiveDb)
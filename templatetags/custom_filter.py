from django import template
from App.models import *
import datetime

register = template.Library()

@register.filter(name="GetOrderPnl")
def GetOrderPnl(OrderObj):
    buy = 0
    sell = 0
    if OrderObj.OrderStatus:
        TransactionObj = Transaction.objects.filter(OrderObj=OrderObj)
        SellOrders = TransactionObj.filter(BuySell='SELL')
        BuyOrders = TransactionObj.filter(BuySell='BUY')
        for i in SellOrders:
            sell = sell + i.TransactionLotSize*i.TransactionLot*i.TriggerPrice
        for j in BuyOrders:
            buy = buy + j.TransactionLotSize*j.TransactionLot*j.TriggerPrice
        
        pnl = sell - buy
    else:
        pnl = 0
    return round(pnl, 2)

@register.filter(name="GetOrderReturns")
def GetOrderReturns(OrderObj):
    buy = 0
    sell = 0
    if OrderObj.OrderStatus:
        TransactionObj = Transaction.objects.filter(OrderObj=OrderObj)
        SellOrders = TransactionObj.filter(BuySell='SELL')
        BuyOrders = TransactionObj.filter(BuySell='BUY')
        for i in SellOrders:
            sell = sell + i.TransactionLotSize*i.TransactionLot*i.TriggerPrice
        for j in BuyOrders:
            buy = buy + j.TransactionLotSize*j.TransactionLot*j.TriggerPrice
        
        pnl = sell - buy
        returns = pnl/buy*100
    else:
        returns = 0

    return round(returns, 2)

@register.filter(name="GetTransactionFromOrder")
def GetTransactionFromOrder(OrderObj):
    TransactionObj = Transaction.objects.filter(OrderObj=OrderObj)
    return TransactionObj

@register.filter(name="GetTransactionCountFromOrder")
def GetTransactionCountFromOrder(OrderObj):
    TransactionObj = Transaction.objects.filter(OrderObj=OrderObj)
    return TransactionObj.count()

@register.filter(name="GetTodaysOrders")
def GetTodaysOrders():
    today = datetime.date.today()
    return Order.objects.filter(CreatedDate__date=today, OrderStatus=True)

@register.filter(name="GetTodaysPnl")
def GetTodaysPnl():
    today = datetime.date.today()
    Orders = Order.objects.filter(CreatedDate__date=today, OrderStatus=True)
    pnl = 0
    for i in Orders:
        pnl = pnl + GetOrderPnl(i)
    
    return round(pnl, 2)

@register.filter(name="GetTodaysReturns")
def GetTodaysReturns():
    today = datetime.date.today()
    Orders = Order.objects.filter(CreatedDate__date=today, OrderStatus=True)
    pnl = 0
    for i in Orders:
        pnl = pnl + GetOrderPnl(i)
    returns = pnl/100000*100
    return round(returns, 2)

@register.filter(name="multiply")
def multiply(n1, n2):
    return round(n1*n2, 2)
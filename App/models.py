from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Configuration(models.Model):

    # =============== GENERAL =================
    ConfigurationName = models.CharField(max_length=100)
    
    # =============== TELEGRAM CREDENTIALS =================
    TelegramToken = models.CharField(max_length=100)

    # =============== ANGLE ONE CREDENTIALS =================
    AngleOneUserName = models.CharField(max_length=100)
    AngleOnePassword = models.CharField(max_length=100)
    AngleOneApiKey = models.CharField(max_length=100)
    AngleOneTotp = models.CharField(max_length=100)
    AngleOneClientId = models.CharField(max_length=100)
    AngleOneClientPin = models.CharField(max_length=100)

    # =============== ANGLE ONE CODE CREDENTIALS =================
    AngleOneAccessToken = models.CharField(max_length=2000, null=True, blank=True)
    AngleOneRefreshToken = models.CharField(max_length=2000, null=True, blank=True)
    AngleOneUserId = models.CharField(max_length=2000, null=True, blank=True)
    AngleOneFeedToken = models.CharField(max_length=100, null=True, blank=True)

    # =============== IMG-TO-TEXT =================
    ImgToTextApiLayer = models.CharField(max_length=100)

    # =============== GOOGLE PALM2 PROMPT =================
    Palm2Api = models.CharField(max_length=100)
    Palm2Model = models.CharField(max_length=100)

    # =============== NGROK BASE URL =================
    NgrokBaseUrl = models.CharField(max_length=100)

    # =============== DATE & TIME =================
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    TokenUpdatedDate = models.DateTimeField(null=True, blank=True)

    ActiveStrategyCodeFor0T1 = models.CharField(max_length=100)
    ActiveStrategyCodeFor0TAll = models.CharField(max_length=100)
    # =============== BALANECE =================
    NormalBalance = models.FloatField(default=0.0)
    HeroZeroBalance = models.FloatField(default=0.0)
    HeroZeroStatus = models.BooleanField(default=False)


    BotStatus = models.BooleanField(default=False)
    FakeLTPStatus = models.BooleanField(default=False)

    # =============== FORCED EXIT =================
    ForcedExitWithoutSelling = models.BooleanField(default=False)
    ForcedExitWithSelling = models.BooleanField(default=False)

    def __str__(self):
        return self.ConfigurationName
    
    class Meta:
        verbose_name = 'Configuration'
        verbose_name_plural = 'Configurations'

    def get_config_obj():
        return Configuration.objects.all().first()
    
class Order(models.Model):
    OrderSymbol = models.CharField(max_length=100)
    OrderStatus = models.BooleanField(default=False)
    StrategyCode = models.CharField(max_length=255)
    CreatedDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.OrderSymbol
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-CreatedDate']

class Transaction(models.Model):
    OrderObj = models.ForeignKey(Order, on_delete=models.CASCADE)
    TransactionSymbol = models.CharField(max_length=100)
    BuySell = models.CharField(max_length=100)
    TransactionLotSize = models.IntegerField()
    TransactionLot = models.IntegerField()
    TriggerPrice = models.FloatField()
    TriggerTime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.TransactionSymbol
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-TriggerTime']
    
class Strategy(models.Model):
    StrategyName = models.CharField(max_length=100)
    StrategyCode = models.CharField(max_length=255, unique=True)
    StrategyDescription = models.TextField(null=True, blank=True)

    SL = models.FloatField()
    TGT = models.FloatField(null=True, blank=True)
    TrailingMargin = models.FloatField(null=True, blank=True)
    TrailingStartAt = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.StrategyName
    
    class Meta:
        verbose_name = 'Strategy'
        verbose_name_plural = 'Strategies'

class LiveDb(models.Model):
    Strategy = models.CharField(max_length=100, null=True, blank=True)
    BUYINGPRICE = models.FloatField(null=True, blank=True)
    LTP = models.FloatField(null=True, blank=True)
    Returns = models.FloatField(null=True, blank=True)
    PNL = models.FloatField(null=True, blank=True)
    SL = models.FloatField(null=True, blank=True)
    FakeLTP = models.FloatField(null=True, blank=True, default=100)
    running = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.BUYINGPRICE = round(self.BUYINGPRICE, 2)
        self.LTP = round(self.LTP, 2)
        self.Returns = round(self.Returns, 2)
        self.PNL = round(self.PNL, 2)
        self.SL = round(self.SL, 2)
        super(LiveDb, self).save(*args, **kwargs)

    def __str__(self):
        return self.Strategy
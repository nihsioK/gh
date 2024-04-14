from django.db import models

    
class Partner(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    card = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    main_category = models.CharField(max_length=100)
    cashback = models.FloatField()
    
    def __str__(self):      
        return self.title


class BankCashback(models.Model):
    category = models.CharField(max_length=100)
    main_category = models.CharField(max_length=100)
    bank = models.CharField(max_length=100)
    card = models.CharField(max_length=100)
    cashback = models.FloatField()
    nfc = models.BooleanField()

    def __str__(self):
        return self.bank
    
class Cards(models.Model):
    bank = models.CharField(max_length=100)
    card = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', related_name='cards', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
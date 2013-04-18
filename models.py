from django.db import models
import datetime
import calendar

#__all__=['MoneyHolder', 'RegularExpenses', 'Aim', "Wallet", "Transactions", "Period"]

class Tag(models.Model):
    name = models.CharField(max_length=200, primary_key=True)
    
    def __unicode__(self):
        return u"{}".format(self.name)

class MoneyHolder(models.Model):
    name = models.CharField(max_length=200, unique=True)
    initial = models.IntegerField()
    amount = models.IntegerField()
    cents = models.IntegerField()
    
    def ReCalculate(self):
        pass
    
    @staticmethod
    def sum_transactions(data):
        ammount = sum(map(lambda x: x.ammount, data))
        cents = sum(map(lambda x: x.cents, data))
        return (ammount, cents)
    
    def get_income(self, period):
        data = Transactions.in_period(period).filter(destination=self.pk)
        return self.sum_transactions(data)
    
    def get_outcome(self, period):
        data = Transactions.in_period(period).filter(source=self.pk)
        return self.sum_transactions(data)
    
    def __unicode__(self):
        return u"{} {}.{}".format(self.name, self.amount, self.cents)

class RegularExpenses(models.Model):
    money = models.ForeignKey(MoneyHolder)
    amount = models.IntegerField()
    cents = models.IntegerField()
    start = models.DateField()
    stop = models.DateField(null=True)
    
    def __unicode__(self):
        return u"{} (from {} to {}): {}.{}".format(self.money.name, self.start, self.stop, self.amount, self.cents)
    
    @classmethod
    def actual(cls, period):
        return cls.objects.filter(models.Q(stop__exact = None) | models.Q(stop__exact = period.date_to), start__lte = period.date_from).order_by('money__name')
    
    def Update(self, amount, cents, start_date):
        
        if self.start.year != start_date.year or self.start.month != start_date.month:
            self.stop = datetime.date(start_date.year,start_date.month, 1)
            self.save()
            return RegularExpenses.objects.create(money=self.money, amount=amount, cents=cents, start=start_date, stop=None)
        else:
            self.amount = amount
            self.cents = cents
            self.save()
    
class Aim(models.Model):
    name = models.CharField(max_length=200, unique=True)
    money = models.ForeignKey(MoneyHolder)
    start = models.DateField()
    stop = models.DateField()
    
    def __unicode__(self):
        return u"{} - {} ({} -> {})".format(self.name, self.money, self.start, self.stop)
    
class Transactions(models.Model):
    description = models.CharField(max_length=300)
    ammount = models.IntegerField()
    cents = models.IntegerField()
    source = models.ForeignKey(MoneyHolder)
    destination = models.ForeignKey(MoneyHolder, related_name="dest_set")
    date = models.DateField()
    
    def __unicode__(self):
        return u"{}.{} ({} -> {})".format(self.ammount, self.cents, self.source, self.destination)
    
    @classmethod
    def in_period(cls, period):
        return cls.objects.filter(date__gte = period.date_from).filter(date__lt = period.date_to)

class Period(object):
    
    def __init__(self, date_from = datetime.date.min, date_to = datetime.date.max):
        self.date_from = date_from
        self.date_to = date_to
    
    @classmethod
    def this_month(cls):
        today = datetime.date.today()
        return cls.specific_month(today.year, today.month)
    
    @staticmethod
    def specific_month(year, month):
        start = datetime.date(year, month, 1)
        days_in_month = calendar.monthrange(year, month)[1]
        end = start + datetime.timedelta(days = days_in_month)
        return Period(start, end)
        
    def __str__(self):
        return unicode(self)
    
    def __repr__(self):
        return "<Period {}>".format(self)
    
    def __unicode__(self):
        return u"{} -> {}".format(self.date_from, self.date_to)

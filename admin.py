from easyfin.models import RegularExpenses, MoneyHolder, Transactions
from django.contrib import admin

class RegularExpensesAdmin(admin.ModelAdmin):
    pass

admin.site.register(RegularExpenses)
admin.site.register(MoneyHolder)
admin.site.register(Transactions)

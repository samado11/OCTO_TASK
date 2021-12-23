from django.contrib import admin

# Register your models here.
from .models import Loan,Payment,Client,Account

admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(Client)
admin.site.register(Account)
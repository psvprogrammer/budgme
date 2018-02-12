from django.contrib import admin

from .models import Budget, IncomeCategory, OutcomeCategory,\
    Income, Outcome, Period, Profile, BudgetRuleSet, BudgetAccess


admin.site.register(Budget)
admin.site.register(IncomeCategory)
admin.site.register(OutcomeCategory)
admin.site.register(Income)
admin.site.register(Outcome)
admin.site.register(Period)
admin.site.register(Profile)
admin.site.register(BudgetRuleSet)
# admin.site.register(BudgetAccess)

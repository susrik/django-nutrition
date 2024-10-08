from django.contrib import admin
from .models import Food, Meal, Portion, Preferences


class PortionAdmin(admin.ModelAdmin):
    list_display = ("date", "food", "quantity", "meal", "user")
    list_filter = ["date"]


admin.site.register(Food)
admin.site.register(Meal)
admin.site.register(Portion, PortionAdmin)
admin.site.register(Preferences)

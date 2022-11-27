from django.contrib import admin
from . import models

@admin.register(models.Work)
class WorkAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Yearwage)
class YearwageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Wage)
class WageAdmin(admin.ModelAdmin):
    pass

@admin.register(models.total_yukyu)
class YukyuAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Zangyo)
class zangyoAdmin(admin.ModelAdmin):
    pass

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass

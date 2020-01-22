from django.contrib import admin
from . import models

# Register your models here.

class GuideAdmin(admin.ModelAdmin):
    list_display = ("user", )

class ManagerAdmin(admin.ModelAdmin):
    list_display = ("user", )

class SchoolAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class TourAdmin(admin.ModelAdmin):
    list_display = ("id", )

class GuideApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", )


admin.site.register(models.Guide, GuideAdmin)
admin.site.register(models.Manager, ManagerAdmin)
admin.site.register(models.School, SchoolAdmin)
admin.site.register(models.Tour, TourAdmin)
admin.site.register(models.GuideApplication, GuideApplicationAdmin)
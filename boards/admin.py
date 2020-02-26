from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
@admin.register(models.Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]

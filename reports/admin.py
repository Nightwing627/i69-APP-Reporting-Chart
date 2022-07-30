from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Register your models here.

from .models import *

from easy_select2 import select2_modelform

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(Reported_Users)
class Reported_UsersAdmin(ImportExportModelAdmin, ExportActionMixin,admin.ModelAdmin):
    pass
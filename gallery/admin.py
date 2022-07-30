from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Register your models here.

from .models import *

from easy_select2 import select2_modelform

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


# @admin.register(Photo)
# class PhotAdmin(ImportExportModelAdmin, ExportActionMixin,admin.ModelAdmin):
#     pass

@admin.register(Album)
class AlbumAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass

class PhotoAdmin(admin.ModelAdmin):    
    list_display = ['image_tag']
    search_fields = ['user__id','user__username']

admin.site.register(Photo,PhotoAdmin)

from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(age)
class AgeAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(height)
class HeightAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(config)
class ConfigAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(gender)
class GenderAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(searchGender)
class searchGenderAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(tags)
class TagAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ['id', 'tag', 'tag_fr']
    search_fields = ['id', 'tag', 'tag_fr']


@admin.register(ethnicity)
class EthnicityAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(politics)
class PoliticsAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(religious)
class ReligiousAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(music)
class MusicAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(tvShows)
class TVShowAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(book)
class BookAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(movies)
class MoviesAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(sportsTeams)
class SportTeamsAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(zodiacSign)
class zodiacSignAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(family)
class FamilyAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


@admin.register(interestedIn)
class InterestedInAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    list_display = ['id', 'interest', 'interest_fr']

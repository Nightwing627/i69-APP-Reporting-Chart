from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

# Register your models here.
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.db import router, transaction
from django.utils.translation import gettext, gettext_lazy as _
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib import admin, messages
from django.urls import path, reverse
from django.utils.html import escape
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.template.response import TemplateResponse
from django.contrib.admin.options import IS_POPUP_VAR


from .models import *

from easy_select2 import select2_modelform

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


@admin.register(User)
class UserAdmin(ModelAdmin):
    change_user_password_template = None
    list_display = [
        "fullName",
        "socialProvider",
        "gender",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    ]

    help_texts = {"password": "bla bla"}
    # fieldsets = [
    #     (
    #         "Password", {
    #             "fields": ("password",), 
    #             "description": "bla bla"
    #             })
    # ]
    readonly_fields = ("id", "password")
    search_fields = ["id", "username", "fullName", "email"]
    exclude = ('password',)
    filter_horizontal = ("blockedUsers",)
    change_password_form = AdminPasswordChangeForm

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        defaults.update(kwargs)
        # add password hint text
        defaults.update({'help_texts': {'password': 'To change password use <a href="../password">this form</a>'}})
        return super().get_form(request, obj, **defaults)

    def get_urls(self):
        return [
            path(
                "<id>/password/",
                self.admin_site.admin_view(self.user_change_password),
                name="auth_user_password_change",
            ),
        ] + super().get_urls()

    def lookup_allowed(self, lookup, value):
        # Don't allow lookups involving passwords.
        return not lookup.startswith("password") and super().lookup_allowed(
            lookup, value
        )

    @sensitive_post_parameters_m
    @csrf_protect_m
    def add_view(self, request, form_url="", extra_context=None):
        with transaction.atomic(using=router.db_for_write(self.model)):
            return self._add_view(request, form_url, extra_context)

    def _add_view(self, request, form_url="", extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    "order to add users, Django requires that your user "
                    'account have both the "Add user" and "Change user" '
                    "permissions set."
                )
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        username_field = self.model._meta.get_field(self.model.USERNAME_FIELD)
        defaults = {
            "auto_populated_fields": (),
            "username_help_text": username_field.help_text,
        }
        extra_context.update(defaults)
        return super().add_view(request, form_url, extra_context)

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=""):
        user = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, user):
            raise PermissionDenied
        if user is None:
            raise Http404(
                _("%(name)s object with primary key %(key)r does not exist.")
                % {
                    "name": self.model._meta.verbose_name,
                    "key": escape(id),
                }
            )
        if request.method == "POST":
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = gettext("Password changed successfully.")
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        "%s:%s_%s_change"
                        % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {"fields": list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            "title": _("Change password: %s") % escape(user.get_username()),
            "adminForm": adminForm,
            "form_url": form_url,
            "form": form,
            "is_popup": (IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET),
            "add": True,
            "change": False,
            "has_delete_permission": False,
            "has_change_permission": True,
            "has_absolute_url": False,
            "opts": self.model._meta,
            "original": user,
            "save_as": False,
            "show_save": True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template
            or "admin/auth/user/change_password.html",
            context,
        )


@admin.register(UserSocialProfile)
class UserSocialProfileAdmin(
    ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin
):
    pass


@admin.register(CoinSettings)
class CoinSettingsAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    pass


admin.site.register(UserRole)

# admin.site.register(UserPhoto)

@admin.register(UserPhoto)
class UserPhotoAdmin(ModelAdmin):
    list_display = ('id', 'user', 'file_url')
    search_fields = ["user__username", "user__fullName", "user__email"]
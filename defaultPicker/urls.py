from django.urls import path
from defaultPicker.api_view import default_picker_view


urlpatterns = [
    path("pickers/", default_picker_view, name="default_picker"),
]

from django.urls import path
from user import views

urlpatterns = [
    path("signup/", views.worker_signup_view, name="signup"),    
    path("invitation/", views.generate_worker_invitation_view, name="generate_worker_invitation"),
    path("invitation/<str:key>/", views.generate_worker_invitation_view, name="apply_worker_invitation"),
    path("", views.worker_list_view, name="worker_list"),
    path("<str:id>/", views.user_detail_view, name="user_detail"),
]

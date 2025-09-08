from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("predict/", views.predict, name="predict"),
    path("health/", views.health, name="health"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]

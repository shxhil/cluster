from django.urls import path
from publicuser import views


urlpatterns = [
    path("",views.CustomerRegView.as_view(),name="register")
]
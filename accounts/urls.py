from django.urls import path
from accounts import views

urlpatterns = [
    path("send_email", view=views.send_login_email, name="send_login_email"),
    path("login", view=views.login, name="login"),
    path("logout", view=views.logout, name="logout"),
]

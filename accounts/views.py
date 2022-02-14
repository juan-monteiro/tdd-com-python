import uuid
import sys
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from accounts.models import Token


def send_login_email(request: HttpRequest) -> HttpResponse:
    email: str = request.POST["email"]
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print(f"saving uid {uid} for email {email}", file=sys.stderr)
    url = request.build_absolute_uri(f"/accounts/login?uid={uid}")
    send_mail(
        subject="Your login link for Superlists",
        message=f"Use this link to log in: {url}",
        from_email="superlists@jmonteiro.net",
        recipient_list=[email],
        fail_silently=False,
    )
    return render(request, "login_email_sent.html")


def login(request: HttpRequest) -> HttpResponse:
    print("login view", file=sys.stderr)
    uid = request.GET.get("uid")
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect("/")


def logout(request: HttpRequest) -> HttpResponse:
    auth_logout(request=request)
    return redirect("/")

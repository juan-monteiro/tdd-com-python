import sys
from django.contrib.auth.backends import BaseBackend
from accounts.models import ListUser, Token


class PasswordlessAuthenticationBackend(BaseBackend):
    def authenticate(self, request, uid: str) -> ListUser | None:
        print(f"auth uid: {uid}", file=sys.stderr)
        if not Token.objects.filter(uid=uid).exists():
            print("no token found", file=sys.stderr)
            return None
        token = Token.objects.get(uid=uid)
        print("got token", file=sys.stderr)
        try:
            user = ListUser.objects.get(email=token.email)
            print("go user", file=sys.stderr)
            return user
        except ListUser.DoesNotExist:
            print("new user", file=sys.stderr)
            return ListUser.objects.create(email=token.email)

    def get_user(self, email: str) -> ListUser:
        return ListUser.objects.get(email=email)

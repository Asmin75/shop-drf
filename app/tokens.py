from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class TokenGenerator(Token):
    def make_token(self, user):
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

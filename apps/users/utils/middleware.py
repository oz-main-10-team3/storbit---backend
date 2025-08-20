from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import AccessToken

from apps.users.models import User


# WebSocket 연결 시 JWT 토큰을 검증해서 scope['user']에 User를 넣어주는 미들웨어
class JWTAuthMiddleware(BaseMiddleware):
    """
    WebSocket 연결 시 QueryString에 담긴 JWT 토큰을 검증해서
    scope["user"]에 User 객체를 넣어주는 Channels 미들웨어
    """

    async def __call__(self, scope, receive, send):
        # Query string 파싱
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token")

        if token:
            scope["user"] = await self.get_user(token[0])
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)
            close_old_connections()
            return user
        except Exception:
            return AnonymousUser()

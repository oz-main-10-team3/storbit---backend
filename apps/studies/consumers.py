import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from django_redis import get_redis_connection

from apps.studies.models import Study


class StudyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.study_id = self.scope["url_route"]["kwargs"]["study_id"]
        self.room_group_name = f"study_{self.study_id}"
        self.conn = get_redis_connection("default")

        user = self.scope["user"]

        if user.is_authenticated:
            await self.accept()
            await self.send(json.dumps({"message": f"Welcome {user.email}!"}))
        else:
            # 인증 실패 -> 403 처리
            await self.close(code=403)

        self.user_key = user.email
        # study 확인
        try:
            study = await self.get_study(self.study_id)
        except ObjectDoesNotExist:
            await self.close()
            return

        # is_live 검증
        if not study.is_live:
            await self.close()
            return

        # 현재 인원 확인
        current_count = self.conn.scard(self.room_group_name)
        if current_count >= study.member:
            await self.close()
            return

        # 집합에 추가
        self.conn.sadd(self.room_group_name, self.user_key)

        # 다시 인원 확인 (동시 요청 대비)
        current_count = self.conn.scard(self.room_group_name)
        if current_count > study.member:
            self.conn.srem(self.room_group_name, self.user_key)
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def mission_created(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "mission_created",
                    "mission": event["mission"],
                }
            )
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get("type")

        # ["draw:pen","draw:circle"]
        if msg_type in ["draw:pen", "draw:circle"]:
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "draw_message", "msg_type": msg_type, "data": data["data"]}
            )

    async def draw_message(self, event):
        await self.send(text_data=json.dumps({"type": event["msg_type"], "data": event["data"]}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        try:
            self.conn.srem(self.room_group_name, self.user_key)
        except Exception:
            pass

    @sync_to_async
    def get_study(self, study_id):
        return Study.objects.get(pk=study_id)

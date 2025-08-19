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
        self.user_key = f"{self.channel_name}"  # 고유 식별자

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
        await self.accept()

    async def mission_created(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "mission_created",
                    "mission": event["mission"],
                }
            )
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        try:
            self.conn.srem(self.room_group_name, self.user_key)
        except Exception:
            pass

    @sync_to_async
    def get_study(self, study_id):
        return Study.objects.get(pk=study_id)

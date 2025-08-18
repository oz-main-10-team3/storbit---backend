import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist

from apps.studies.models import Study


class StudyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.study_id = self.scope["url_route"]["kwargs"]["study_id"]
        self.room_group_name = f"study_{self.study_id}"

        try:
            await self.get_study(self.study_id)
        except ObjectDoesNotExist:
            await self.close()  # 연결 즉시 종료
            return

        # 그룹에 참가
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # 그룹에서 제거
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @sync_to_async
    def get_study(self, study_id):
        return Study.objects.get(pk=study_id)

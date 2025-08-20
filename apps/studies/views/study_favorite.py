from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.studies.models import Study, StudyFavorite
from apps.studies.serializers.study_favorite import StudyFavoriteSerializer


class StudyFavoriteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["스터디 찜"],
        summary="스터디 찜하기",
    )
    def post(self, request, study_id: int):
        study = Study.objects.filter(pk=study_id).first()
        if not study:
            return Response({"detail": "존재하지 않는 스터디입니다."}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = StudyFavorite.objects.get_or_create(
            user=request.user, study=study, defaults={"is_active": True}
        )

        if created:
            data = StudyFavoriteSerializer(favorite).data
            return Response(data, status=status.HTTP_201_CREATED)

        if favorite.is_active:
            return Response(
                {"detail": "이미 찜한 상태입니다."},
                status=status.HTTP_409_CONFLICT,
            )

        favorite.is_active = True
        favorite.save(update_fields=["is_active"])
        data = StudyFavoriteSerializer(favorite).data
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["스터디 찜"],
        summary="스터디 찜 해제",
    )
    def delete(self, request, study_id: int):
        favorite = StudyFavorite.objects.filter(user=request.user, study_id=study_id, is_active=True).first()
        if not favorite:
            return Response(
                {"detail": "활성화된 찜이 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        favorite.is_active = False
        favorite.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)

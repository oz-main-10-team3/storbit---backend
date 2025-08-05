from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Study
from .serializers import StudyApplicationSerializer


class StudyApplicationCreateView(APIView):
    """
    스터디 신청을 생성하는 API 뷰
    """

    def post(self, request, study_id):
        study_instance = get_object_or_404(Study, pk=study_id)

        serializer = StudyApplicationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # study_instance를 context가 아닌 save() 메소드의 인자로 전달
                serializer.save(study=study_instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

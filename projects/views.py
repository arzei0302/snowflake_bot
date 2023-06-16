from rest_framework.viewsets import ModelViewSet
from projects.models import Project, UserAppeal
from projects.serializers import ProjectSerializer, UserAppealSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import timedelta, datetime


class ProjectView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class UserAppealView(ModelViewSet):
    queryset = UserAppeal.objects.all()
    serializer_class = UserAppealSerializer

    @action(methods=['get', ], detail=False)
    def get_week(self, request, *args, **kwargs):
        user_appeal = UserAppeal.objects.filter(date__lte=datetime.now(), date__gte=datetime.now()-timedelta(days=7))
        serializer = UserAppealSerializer(user_appeal, many=True).data
        return Response(serializer, status=200)
    

    @action(methods=['get', ], detail=False)
    def get_month(self, request, *args, **kwargs):
        user_appeal = UserAppeal.objects.filter(date__lte=datetime.now(), date__gte=datetime.now()-timedelta(days=30))
        serializer = UserAppealSerializer(user_appeal, many=True).data
        return Response(serializer, status=200)
    

    @action(methods=['get', ], detail=False)
    def get_year(self, request, *args, **kwargs):
        user_appeal = UserAppeal.objects.filter(date__lte=datetime.now(), date__gte=datetime.now()-timedelta(days=365))
        serializer = UserAppealSerializer(user_appeal, many=True).data
        return Response(serializer, status=200)
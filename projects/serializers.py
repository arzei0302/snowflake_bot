from rest_framework import serializers
from .models import Project, UserAppeal

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'photo', 'is_approved',)


class UserAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAppeal
        fields = ('id', 'name', 'mail', 'message', 'date',)
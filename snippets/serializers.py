from rest_framework.serializers import ModelSerializer
from .models import Group


class GetGroups(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'logo', 'type')
        read_only_fields = ('id', 'name', 'logo', 'type')

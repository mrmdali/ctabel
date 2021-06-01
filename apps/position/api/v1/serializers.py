from rest_framework import serializers
from apps.position.models import Position


class PositionSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = ('id', 'name', 'status', 'description', 'date_created')

    def get_status(self, obj):
        return obj.get_status_display()
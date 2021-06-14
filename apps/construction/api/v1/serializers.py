from rest_framework import serializers
from ...models import Construction, Object


class ObjectSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Object
        fields = ('id', 'name', 'status', 'description', 'date_created')

    def get_status(self, obj):
        return obj.get_status_display()


class ObjectDetailSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Object
        fields = ('id', 'status')

    def get_status(self, obj):
        return obj.get_status_display()


class ConstructionSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Construction
        fields = ('id', 'object', 'name', 'status', 'description', 'date_created')

    def get_status(self, obj):
        return obj.get_status_display()


class ConstructionDetailSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Construction
        fields = ('id', 'status')

    def get_status(self, obj):
        return obj.get_status_display()
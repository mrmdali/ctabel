from rest_framework import serializers
from rest_framework.response import Response

from apps.account.models import Worker
from ...models import (
    WorkingHour,
    Attendance,
    Reason,
    ReasonToNoAttendance,
)


class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = ('id', 'hour', 'date_modified', 'date_created')


class AttendanceSerializer(serializers.ModelSerializer):
    header_worker_full_name = serializers.CharField(source='header_worker.get_full_name', read_only=True)
    worker_full_name = serializers.CharField(source='worker.get_full_name', read_only=True)
    construction_name = serializers.CharField(source='construction.name', read_only=True)

    class Meta:
        model = Attendance
        fields = ('id', 'header_worker', 'header_worker_full_name', 'worker', 'worker_full_name', 'construction',
                  'construction_name', 'checkin', 'checkout', 'working_hours', 'date_modified', 'date_created')
        extra_kwargs = {
                'header_worker': {'required': False},
                'worker': {'required': True},
        }


class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'reason', 'date_modified', 'date_created')


class ReasonToNoAttendanceListSerializer(serializers.ModelSerializer):
    attendance = AttendanceSerializer()
    reason = serializers.CharField(source='reason.reason', read_only=True)

    class Meta:
        model = ReasonToNoAttendance
        fields = ('id', 'attendance', 'reason', 'context', 'date_modified', 'date_created')


class ReasonToNoAttendanceCreateSerializer(serializers.ModelSerializer):
    attendance = AttendanceSerializer()
    reason_name = serializers.CharField(source='reason.reason', read_only=True)

    class Meta:
        model = ReasonToNoAttendance
        fields = ('id', 'attendance', 'reason', 'reason_name', 'context', 'date_modified', 'date_created')

    def create(self, validated_data):
        request = self.context['request']
        user_id = request.user.id
        header_worker = Worker.objects.get(account_id=user_id)

        attendance_data = validated_data.pop('attendance')
        attendance = Attendance.objects.create(header_worker=header_worker, worker=attendance_data['worker'])
        data = ReasonToNoAttendance.objects.create(attendance=attendance,
                                                   reason=validated_data.pop('reason'),
                                                   context=validated_data.pop('context'),
                                                   )
        return data


class ReasonToNoAttendanceDetailSerializer(serializers.ModelSerializer):
    attendance = AttendanceSerializer(read_only=True)
    reason_name = serializers.CharField(source='reason.reason', read_only=True)

    class Meta:
        model = ReasonToNoAttendance
        fields = ('id', 'attendance', 'reason', 'reason_name', 'context', 'date_modified', 'date_created')



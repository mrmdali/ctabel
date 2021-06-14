from rest_framework.response import Response
from rest_framework.views import APIView

from apps.account.models import Worker
from apps.basic.permissions import IsOwnerOrReadOnlyForEditingAttendance
from .serializers import (
    WorkingHourSerializer,
    AttendanceSerializer,
    ReasonSerializer,
    ReasonToNoAttendanceListSerializer, ReasonToNoAttendanceCreateSerializer, ReasonToNoAttendanceDetailSerializer
)
from ...models import (
    WorkingHour,
    Attendance,
    Reason,
    ReasonToNoAttendance,
)
from rest_framework import generics, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)


class WorkingHourListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/attendance/v1/working-hour-list/

    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer
    permission_classes = (IsAuthenticated, )


class WorkingHourCreateView(generics.CreateAPIView):
    # http://127.0.0.1:8000/api/attendance/v1/working-hour-create/

    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer
    permission_classes = (IsAdminUser, )


class WorkingHourRUDView(generics.RetrieveUpdateDestroyAPIView):
    # http://127.0.0.1:8000/api/attendance/v1/working-hour-rud/{id}/

    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer
    permission_classes = (IsAdminUser, )


class AttendanceListCreateView(generics.ListCreateAPIView):
    # http://127.0.0.1:8000/api/attendance/v1/attendance-list-create/

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        user = self.request.user
        attendance = Attendance.objects.filter(header_worker__account=user)
        print(attendance)
        sz = self.get_serializer(attendance, many=True)
        return Response(sz.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            user = self.request.user
            header_workers = Worker.objects.filter(header_worker__account_id=user.id)
        except Exception as e:
            return Response({'error': e.args})
        else:
            for i in request.data:
                sz = self.get_serializer(data=i)
                if sz.is_valid():
                    if sz.validated_data['worker'] in header_workers:
                        sz.save(header_worker=user.workers)
                        # return Response(sz.data, status=status.HTTP_201_CREATED)
                    # return Response({'error': 'worker is not allowed to the header worker'},
                    #                 status=status.HTTP_406_NOT_ACCEPTABLE)
                # return Response({'error': 'serializer is not a valid'}, status=status.HTTP_409_CONFLICT)
            return Response({'success': 'Successfully created'})


class AttendanceRUDView(generics.RetrieveUpdateDestroyAPIView):
    # http://127.0.0.1:8000/api/attendance/v1/attendance-rud/{id}/

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyForEditingAttendance)

    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.request.user
            header_worker = Worker.objects.get(account_id=user.id)
            qs = self.get_object()
            sz = self.get_serializer(qs)
            if sz.data['header_worker_id'] == header_worker.id:
                return Response(sz.data, status=status.HTTP_200_OK)
            return Response({'error': 'query not match for the header worker'})
        except Exception as e:
            return Response({'error': e.args})

    def update(self, request, *args, **kwargs):
        user = self.request.user
        header_worker = Worker.objects.get(account_id=user.id)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        sz = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            if sz.is_valid():
                if instance.header_worker.id == header_worker.id:
                    sz.save()
                    return Response(sz.data, status=status.HTTP_202_ACCEPTED)
                return Response({'error': 'query is not match for the header worker'})
            return Response({'error': 'serializer is not a valid'})
        except Exception as e:
            return Response({'error': e.args})

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        header_worker = Worker.objects.get(account_id=user.id)
        instance = self.get_object()
        try:
            if instance.header_worker.id == header_worker.id:
                instance.delete()
                return Response({'error': 'successfully deleted', 'status': status.HTTP_200_OK})
            return Response({'error': 'query is not match for the header worker'})
        except Exception as e:
            return Response({'error': e.args})


class ReasonListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/attendance/v1/reason-list/

    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer
    permission_classes = (IsAuthenticated, )


class ReasonCreateView(generics.CreateAPIView):
    # http://127.0.0.1:8000/api/attendance/v1/reason-create/

    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer
    permission_classes = (IsAdminUser, )


class ReasonRUDView(generics.RetrieveUpdateDestroyAPIView):
    # http://127.0.0.1:8000/api/attendance/v1/reason-rud/{id}/

    queryset = Reason.objects.all()
    serializer_class = ReasonSerializer
    permission_classes = (IsAdminUser, )


class ReasonToNoAttendanceAllListView(APIView):
    # http://127.0.0.1:8000/api/attendance/v1/no-attendance-all-list/

    queryset = ReasonToNoAttendance.objects.order_by('-id')
    serializer_class = ReasonToNoAttendanceListSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            qs = self.queryset.all()
            sz = self.serializer_class(qs, many=True)
        except Exception as e:
            return Response({'error': e.args})
        else:
            return Response(sz.data, status=status.HTTP_200_OK)


class ReasonToNoAttendanceSelfListView(APIView):
    # http://127.0.0.1:8000/api/attendance/v1/no-attendance-self-list/

    serializer_class = ReasonToNoAttendanceListSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            qs = ReasonToNoAttendance.objects.filter(attendance__header_worker__account_id=user.id)
            sz = self.serializer_class(qs, many=True)
        except Exception as e:
            return Response({'error': e.args})
        else:
            return Response(sz.data, status=status.HTTP_200_OK)


class ReasonToNoAttendanceSelfCreateListView(generics.CreateAPIView):
    # http://127.0.0.1:8000/api/attendance/v1/no-attendance-self-create/

    serializer_class = ReasonToNoAttendanceCreateSerializer
    # permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        try:
            user_id = request.user.id
            header_worker = Worker.objects.filter(header_worker__account_id=user_id)
            sz = self.serializer_class(data=request.data, context={"request": self.request})
        except Exception as e:
            return Response({'error': e.args})
        else:
            if sz.is_valid():
                if sz.validated_data['attendance']['worker'] in header_worker:
                    sz.save()
                    return Response(sz.data, status=status.HTTP_201_CREATED)
                return Response({'error': 'worker is not allowed to the header worker'})
            return Response('Something get wrong, values not a valid')


class ReasonToNoAttendanceRUDView(generics.RetrieveUpdateDestroyAPIView):
    # http://127.0.0.1:8000/api/attendance/v1/no-attendance-rud/{id}/

    queryset = ReasonToNoAttendance.objects.all()
    serializer_class = ReasonToNoAttendanceDetailSerializer
    # permission_classes = (IsAuthenticated, )

    def retrieve(self, request, *args, **kwargs):
        try:
            user_id = self.request.user.id
            header_worker = Worker.objects.get(account_id=user_id)
            qs = self.get_object()
            sz = self.get_serializer(qs)
            if sz.data['attendance']['header_worker'] == header_worker.id:
                return Response(sz.data, status=status.HTTP_200_OK)
            return Response({'error': 'query not match for the header worker'})
        except Exception as e:
            return Response({'error': e.args})

    def update(self, request, *args, **kwargs):
        user_id = self.request.user.id
        header_worker = Worker.objects.get(account_id=user_id)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        sz = self.get_serializer(instance, data=request.data, partial=partial)
        try:
            if sz.is_valid():
                if instance.attendance.header_worker.id == header_worker.id:
                    sz.save()
                    return Response(sz.data, status=status.HTTP_202_ACCEPTED)
                return Response({'error': 'query is not match for the header worker'})
            return Response({'error': 'serializer is not a valid'})
        except Exception as e:
            return Response({'error': e.args})

    def delete(self, request, *args, **kwargs):
        user_id = self.request.user.id
        header_worker = Worker.objects.get(account_id=user_id)
        instance = self.get_object()
        try:
            if instance.attendance.header_worker.id == header_worker.id:
                instance.delete()
                return Response({'error': 'successfully deleted', 'status': status.HTTP_200_OK})
            return Response({'error': 'query is not match for the header worker'})
        except Exception as e:
            return Response({'error': e.args})



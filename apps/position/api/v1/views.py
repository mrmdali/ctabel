from django.db.models import Q
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.position.api.v1.serializers import PositionSerializer
from apps.position.models import Position


class PositionListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/position/v1/position-list/
    queryset = Position.objects.filter(status=0)
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = self.queryset.all()
        param = self.request.GET.get('q')
        if param:
            try:
                queryset = queryset.order_by(param)
            except Exception:
                return []
        return queryset


class PositionInactiveListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/position/v1/position-inactive-list/
    queryset = Position.objects.filter(status=1)
    serializer_class = PositionSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = self.queryset.all()
        param = self.request.GET.get('q')
        if param:
            try:
                queryset = queryset.order_by(param)
            except Exception:
                return []
        return queryset


class PositionCreateView(generics.CreateAPIView):
    # http://127.0.0.1:8000/api/position/v1/position-create/
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsAdminUser, )


class PositionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    # http://127.0.0.1:8000/api/position/v1/position-retrieve-update/{id}/
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsAdminUser, )


class PositionDeleteView(APIView):
    # http://127.0.0.1:8000/api/position/v1/position-delete/{id}/

    permission_classes = (IsAdminUser, )

    def put(self, request, pk, *args, **kwargs):
        # user = self.request.user
        # qs = Worker.objects.get(account=user)
        try:
            qs = Position.objects.get(Q(id=pk) & Q(status=0))
        except Exception as e:
            return Response({'error': e.args})
        else:
            if qs.position_workers.count() == 0:
                print(qs.position_workers.count())
                serializer = PositionSerializer(qs, data=request.data)
                if serializer.is_valid():
                    serializer.save(status=1)
                    return Response({'success': 'Successfully deleted'})
                return Response({'error': 'Serializer is not a valid', 'sz_errors': serializer.errors})
            return Response({'error': 'the position has workers'})


class PositionActivateView(APIView):
    # http://127.0.0.1:8000/api/position/v1/position-activate/{id}/

    permission_classes = (IsAdminUser, )

    def put(self, request, pk, *args, **kwargs):
        # user = self.request.user
        # qs = Worker.objects.get(account=user)
        qs = Position.objects.get(Q(id=pk) & Q(status=1))
        if qs:
            serializer = PositionSerializer(qs, data=request.data)
            if serializer.is_valid():
                serializer.save(status=0)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return request(status.HTTP_404_NOT_FOUND)

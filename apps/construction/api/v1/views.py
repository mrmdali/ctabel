from django.db.models import Q
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

from .serializers import ConstructionSerializer, ConstructionDetailSerializer
from ...models import Construction


class ConstructionListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/construction/v1/construction-list/

    queryset = Construction.objects.order_by('-id')
    serializer_class = ConstructionSerializer
    permission_classes = (IsAuthenticated,)


class ConstructionActiveListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/construction/v1/construction-list-active/

    queryset = Construction.objects.filter(status=0).order_by('-id')
    serializer_class = ConstructionSerializer
    permission_classes = (IsAuthenticated,)


class ConstructionInactiveListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/construction/v1/construction-list-inactive/

    queryset = Construction.objects.filter(status=1).order_by('-id')
    serializer_class = ConstructionSerializer
    permission_classes = (IsAuthenticated,)


class ConstructionCreateView(generics.CreateAPIView):
    # http://127.0.0.1:8000/api/construction/v1/construction-create/

    queryset = Construction.objects.all()
    serializer_class = ConstructionSerializer
    permission_classes = (IsAdminUser, )


class ConstructionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    # http://127.0.0.1:8000/api/construction/v1/construction-retrieve-update/{id}/

    queryset = Construction.objects.all()
    serializer_class = ConstructionSerializer
    permission_classes = (IsAdminUser, )


class ConstructionInactivateView(APIView):
    # http://127.0.0.1:8000/api/construction/v1/construction-inactivate/{id}/

    permission_classes = (IsAdminUser, )

    def put(self, request, pk, *args, **kwargs):
        # user = self.request.user
        # qs = Worker.objects.get(account=user)
        try:
            qs = Construction.objects.get(Q(id=pk) & Q(status=0))
        except Exception as e:
            return Response({'error': e.args})
        else:
            if qs.construction_workers.count() == 0:
                serializer = ConstructionDetailSerializer(qs, data=request.data)
                if serializer.is_valid():
                    serializer.save(status=1)
                    return Response('Successfully inactivated')
                return Response('Serializer is not a valid')
            return Response({'error': 'the construction has workers'})


class ConstructionActivateView(APIView):
    # http://127.0.0.1:8000/api/construction/v1/construction-activate/{id}/

    permission_classes = (IsAdminUser, )

    def put(self, request, pk, *args, **kwargs):
        # user = self.request.user
        # qs = Worker.objects.get(account=user)
        try:
            qs = Construction.objects.get(Q(id=pk) & Q(status=1))
        except Exception as e:
            return Response({'error': e.args})
        else:
            serializer = ConstructionDetailSerializer(qs, data=request.data)
            if serializer.is_valid():
                serializer.save(status=0)
                return Response('Successfully activated')
            return Response('Serializer is not a valid')

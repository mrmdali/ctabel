from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.attendance.models import Attendance
from .serializers import AccountRegisterSerializer, WorkerListSerializer, WorkerDetailSerializer, \
    WorkerUpdateSerializer, AccountUpdateSerializer, ChangePasswordSerializer, WorkerDismissSerializer
from ...models import Worker, Account, Position


class AccountRegisterView(APIView):
    # http://127.0.0.1:8000/api/account/v1/account-register/
    permission_classes = (IsAdminUser, )

    def post(self, request):
        serializer = AccountRegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            if account:
                pk = account.id
                worker = Worker.objects.get(account_id=pk).id
                # return Response(serializer.data, status=status.HTTP_201_CREATED)
                print(HttpResponseRedirect(redirect_to=f'/api/account/v1/worker-detail-update/{worker}/'))
                return HttpResponseRedirect(redirect_to=f'/api/account/v1/worker-detail-update/{worker}/')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class AccountDetailUpdateView(APIView):
    # http://127.0.0.1:8000/api/account/v1/account-detail-update/{id}/
    permission_classes = (IsAdminUser, )

    def get(self, request, pk, *args, **kwargs):
        # user = self.request.user
        # qs = Account.objects.get(id=user.id)
        qs = Account.objects.get(id=pk)
        if qs:
            serializer = AccountRegisterSerializer(qs)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        # user = self.request.user
        # qs = Account.objects.get(id=user.id)
        qs = Account.objects.get(id=pk)
        if qs:
            serializer = AccountUpdateSerializer(qs, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return request(status.HTTP_404_NOT_FOUND)


class ChangePasswordView(generics.UpdateAPIView):
    # http://127.0.0.1:8000/api/account/v1/account-change-password/{id}/
    queryset = Account.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            serializer = self.get_serializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': 'Password successfully changed'})
        except Exception as e:
            return Response({'error': e.args})


class AllActiveWorkersListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/account/v1/all-active-workers-list/

    serializer_class = WorkerDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Worker.objects.filter(is_dismissed=False).order_by('-id')


class AllInactiveWorkersListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/account/v1/all-inactive-workers-list/

    serializer_class = WorkerDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Worker.objects.filter(is_dismissed=False).order_by('-id')


class DismissedWorkersListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/account/v1/dismissed-workers-list/

    serializer_class = WorkerDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Worker.objects.filter(is_dismissed=True).order_by('-id')


class WorkerListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/account/v1/worker-list/

    serializer_class = WorkerListSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Worker.objects.filter(Q(is_header=True) & Q(is_dismissed=False)).order_by('-id')


class WorkerRetrieveUpdateView(APIView):
    # http://127.0.0.1:8000/api/account/v1/worker-detail-update/{id}/

    permission_classes = (IsAdminUser, )

    def get(self, request, pk, *args, **kwargs):
        # user = self.request.user
        # qs = Worker.objects.get(account=user)
        qs = Worker.objects.get(Q(id=pk) & Q(is_dismissed=False))
        if qs:
            serializer = WorkerDetailSerializer(qs)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, *args, **kwargs):
        # user = self.request.user
        # qs = Worker.objects.get(account=user)
        qs = Worker.objects.get(Q(id=pk) & Q(is_dismissed=False))
        if qs:
            serializer = WorkerUpdateSerializer(qs, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return request(status.HTTP_404_NOT_FOUND)


class SelfWorkersListView(APIView):
    # http://127.0.0.1:8000/api/account/v1/self-workers-list/

    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user = self.request.user
        qs = Worker.objects.filter(Q(header_worker__account=user) & ~Q(subworkers__date_created__date=timezone.now().date()))
        if qs:
            serializer = WorkerDetailSerializer(qs, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class WorkerDismissView(APIView):
    # http://127.0.0.1:8000/api/account/v1/worker-dismiss/{id}/

    permission_classes = (IsAdminUser, )

    def put(self, request, pk, *args, **kwargs):
        # user = self.request.user
        # qs = Worker.objects.get(account=user)
        try:
            qs = Worker.objects.get(Q(id=pk) & Q(is_dismissed=False))
        except Exception as e:
            return Response({'error': e.args})
        else:
            if qs.children.count() == 0:
                serializer = WorkerDismissSerializer(qs, data=request.data)
                if serializer.is_valid():
                    serializer.save(is_dismissed=True)
                    return Response('Successfully dismissed')
                return Response('Serializer is not a valid')
            return Response({'error': 'the worker has sub workers'})


class WorkerActivateView(APIView):
    # http://127.0.0.1:8000/api/account/v1/worker-activate/{id}/

    permission_classes = (IsAdminUser, )

    def put(self, request, pk, *args, **kwargs):
        # user = self.request.user
        # qs = Worker.objects.get(account=user)
        try:
            qs = Worker.objects.get(Q(id=pk) & Q(is_dismissed=True))
        except Exception as e:
            return Response({'error': e.args})
        else:
            serializer = WorkerDismissSerializer(qs, data=request.data)
            if serializer.is_valid():
                serializer.save(is_dismissed=False)
                return Response('Successfully activated')
            return Response('Serializer is not a valid')


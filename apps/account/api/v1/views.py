from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.attendance.models import Attendance
from .serializers import AccountRegisterSerializer, WorkerListSerializer, WorkerDetailSerializer, \
    WorkerUpdateSerializer, AccountUpdateSerializer, ChangePasswordSerializer, WorkerDismissSerializer, \
    WorkerTableListSerializer, TokenGenerateSerializer
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
                # print(HttpResponseRedirect(redirect_to=f'/api/account/v1/worker-detail-update/{worker}/'))
                return HttpResponseRedirect(redirect_to=f'/api/account/v1/worker-detail-update/{worker}/')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class LoginView(TokenObtainPairView):
    serializer_class = TokenGenerateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = Account.objects.filter(username=self.request.data['username']).first()
        password = self.request.data['password']
        if user:
            if not user.is_active:
                return Response({'message': 'The user is not a active'})
        else:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        else:
            data = serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)


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
    queryset = Worker.objects.filter(is_dismissed=False)

    def get_queryset(self):
        queryset = self.queryset.all()
        param = self.request.GET.get('q')
        if param:
            try:
                queryset = queryset.order_by(param)
            except Exception as e:
                return []
        return queryset


class AllInactiveWorkersListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/account/v1/all-inactive-workers-list/

    serializer_class = WorkerDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Worker.objects.filter(is_dismissed=False)

    def get_queryset(self):
        queryset = self.queryset.all()
        param = self.request.GET.get('q')
        if param:
            try:
                queryset = queryset.order_by(param)
            except Exception as e:
                return []
        return queryset


class DismissedWorkersListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/account/v1/dismissed-workers-list/

    serializer_class = WorkerDetailSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Worker.objects.filter(is_dismissed=True)

    def get_queryset(self):
        queryset = self.queryset.all()
        param = self.request.GET.get('q')
        if param:
            try:
                queryset = queryset.order_by(param)
            except Exception as e:
                return []
        return queryset


class WorkerListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/account/v1/worker-list/

    serializer_class = WorkerListSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Worker.objects.filter(Q(is_header=True) & Q(is_dismissed=False))

    def get_queryset(self):
        queryset = self.queryset.all()
        param = self.request.GET.get('q')
        if param:
            try:
                queryset = queryset.order_by(param)
            except Exception as e:
                return []
        return queryset


class WorkerTableListView(generics.ListAPIView):
    # http://127.0.0.1:8000/api/account/v1/worker-table-list/

    serializer_class = WorkerTableListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        queryset = Worker.objects.filter(Q(is_header=True) & Q(is_dismissed=False))
        if queryset:
            return queryset
        return Response({'message': 'Queryset does not exist'})

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset:
            try:
                serializer = self.get_serializer(queryset, many=True, context={'request': request})
                return Response(serializer.data)
            except Exception as e:
                return Response({'message': e.args})
        else:
            return Response({'message': 'queryset is an empty'})


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
        qs = Worker.objects.get(id=pk)
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
            # serializer.data['success'] = True
            return Response(serializer.data, status.HTTP_200_OK)
        return Response({'success': False, 'message': 'The worker has no sub workers'})


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


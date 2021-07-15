from abc import ABC

from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ...models import Account, Worker
from ....attendance.api.v1.serializers import AttendanceTableSerializer
from ....attendance.models import Attendance


class AccountRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    password2 = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password', 'password2')
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'required': False},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields did not match.'})

        return attrs

    def create(self, validated_data):
        try:
            account = Account.objects.create(
                username=validated_data['username'],
                email=validated_data['email']
            )
        except:
            account = Account.objects.create(
                username=validated_data['username'],
            )
        account.set_password(validated_data['password'])
        account.save()
        return account


class AccountSerializer(serializers.ModelSerializer):
    is_header = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('full_name', 'username', 'email', 'is_superuser', 'is_staff', 'is_active', 'is_header')
        extra_kwargs = {
            'full_name': {'read_only': True},
            'username': {'read_only': True},
            'email': {'read_only': True},
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'is_header': {'read_only': True},
        }

    def get_is_header(self, obj):
        return Worker.objects.filter(account=obj).first().is_header

    def get_full_name(self, obj):
        return Worker.objects.filter(account=obj).first().get_full_name


class TokenGenerateSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(TokenGenerateSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        account = AccountSerializer(instance=self.user).data
        if account['is_superuser'] and not account['is_header']:
            data['roll'] = 'superuser'
        elif account['is_header'] and account['is_superuser']:
            data['roll'] = 'staff'
        elif account['is_header'] and not account['is_superuser']:
            data['roll'] = 'staff'
        else:
            data['roll'] = 'worker'

        return data


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'email')


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6,
                                     help_text='length must equal to be 6')
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=6,
                                             help_text='value must be the same with password')

    # old_password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = Account
        fields = ('password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    # def validate_old_password(self, value):
    #     user = self.context['request'].user
    #     if not user.check_password(value):
    #         raise serializers.ValidationError({"old_password": "Old password is not correct"})
    #     return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return Response({'instance': instance})


class WorkerDetailSerializer(serializers.ModelSerializer):
    account = AccountUpdateSerializer(required=False, many=False)
    position_name = serializers.CharField(source='position.name', read_only=True)
    header_worker_name = serializers.CharField(source='header_worker.get_full_name', read_only=True)

    class Meta:
        model = Worker
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'account', 'image', 'phone', 'header_worker_name',
                  'header_worker', 'position', 'position_name', 'is_header', 'is_dismissed')
        extra_kwargs = {
            'account': {
                'read_only': True,
                'required': False
            }
        }


class WorkerTableDetailSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(source='position.name', read_only=True)
    attendance = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_attendance(self, obj):
        request = self.context['request']
        month = request.GET.get('month')
        year = request.GET.get('year')
        construction = request.GET.get('construction')
        if construction:
            if month and year:
                attendances = Attendance.objects.filter(Q(worker=obj) &
                                                        Q(date_created__year=year, date_created__month=month) &
                                                        Q(construction__name__exact=construction))
            else:
                attendances = Attendance.objects.filter(Q(worker=obj) & Q(date_created__year=timezone.now().year,
                                                        date_created__month=timezone.now().month) &
                                                        Q(construction__name__exact=construction))
        else:
            if month and year:
                attendances = Attendance.objects.filter(Q(worker=obj) & Q(date_created__year=year,
                                                                          date_created__month=month))
            else:
                attendances = Attendance.objects.filter(Q(worker=obj) & Q(date_created__year=timezone.now().year,
                                                        date_created__month=timezone.now().month))
        serializer = AttendanceTableSerializer(instance=attendances, many=True).data
        sz = list(serializer)
        self.total = 0
        for i in sz:
            if i['working_hours'] is not None:
                self.total += i['working_hours']
        return sz

    def get_total(self, obj):
        return self.total

    class Meta:
        model = Worker
        fields = ('id', 'get_full_name', 'position_name', 'attendance', 'total')


class WorkerTableListSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    position_name = serializers.CharField(source='position.name', read_only=True)

    def get_children(self, obj):
        request = self.context['request']
        position = request.GET.get('position')
        qs = Worker.objects.filter(is_dismissed=False, header_worker=obj)
        if position:
            qs = Worker.objects.filter(Q(is_dismissed=False) & Q(header_worker=obj) &
                                       Q(position__name__exact=position))
        serializer = WorkerTableDetailSerializer(instance=qs, many=True, context={'request': request})
        return serializer.data

    class Meta:
        model = Worker
        fields = ('id', 'get_full_name', 'position_name', 'children')


class WorkerUpdateSerializer(serializers.ModelSerializer):
    account = AccountUpdateSerializer(required=False, many=False)
    header_worker_name = serializers.CharField(source='header_worker.get_full_name', read_only=True)

    class Meta:
        model = Worker
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'account', 'image', 'phone', 'header_worker',
                  'header_worker_name', 'position', 'is_header', 'is_dismissed')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'header_worker': {'required': False},
            'position': {'required': True},
        }


class WorkerDismissSerializer(serializers.ModelSerializer):
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = ('id', 'is_dismissed', 'children_count')
        extra_kwargs = {
            'is_dismissed': {'required': False},
        }

    def get_children_count(self, obj):
        count = obj
        return count


class WorkerListSerializer(serializers.ModelSerializer):
    account = AccountRegisterSerializer()
    children = serializers.SerializerMethodField()
    # children = WorkerDetailSerializer(many=True)
    construction_name = serializers.CharField(source='construction.name', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)

    def get_children(self, obj):
        qs = Worker.objects.filter(is_dismissed=False, header_worker=obj)
        serializer = WorkerDetailSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Worker
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'account', 'image', 'phone', 'construction_name',
                  'position', 'position_name', 'children', 'is_header', 'is_dismissed')

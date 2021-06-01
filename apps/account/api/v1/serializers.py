from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.response import Response
from ...models import Account, HeaderWorker, SubWorker, Worker


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
    construction_name = serializers.CharField(source='construction.name', read_only=True)
    position_name = serializers.CharField(source='position.name', read_only=True)
    header_worker_name = serializers.CharField(source='header_worker.get_full_name', read_only=True)

    class Meta:
        model = Worker
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'account', 'image', 'phone', 'header_worker_name',
                  'header_worker', 'construction', 'construction_name', 'position', 'position_name', 'is_header',
                  'is_dismissed')
        extra_kwargs = {
            'account': {
                'read_only': True,
                'required': False
            }
        }


class WorkerUpdateSerializer(serializers.ModelSerializer):
    account = AccountUpdateSerializer(required=False, many=False)
    header_worker_name = serializers.CharField(source='header_worker.get_full_name', read_only=True)

    class Meta:
        model = Worker
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'account', 'image', 'phone', 'header_worker',
                  'header_worker_name', 'construction', 'position', 'is_header', 'is_dismissed')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'header_worker': {'required': False},
            'construction': {'required': True},
            'position': {'required': True},
        }


class WorkerDismissSerializer(serializers.ModelSerializer):
    children_count = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = ('id',  'is_dismissed', 'children_count')
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
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'account', 'image', 'phone', 'construction',
                  'construction_name', 'position', 'position_name', 'children', 'is_header', 'is_dismissed')

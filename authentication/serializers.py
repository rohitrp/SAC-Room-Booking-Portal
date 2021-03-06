from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from authentication.models import Account

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'name', 'created_at', 'updated_at',
                  'password', 'confirm_password')
        read_only_fields = ('created_at', 'updated_at')

        def create(self, validated_data):
            print(validated_data)
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.username = validated_data.get('username', instance.username)
            instance.is_admin = validated_data.get('is_admin', instance.is_admin)
            instance.is_gsec = validated_data.get('is_admin', instance.is_gsec)
            instance.is_verified = validated_data.get('is_admin', instance.is_gsec)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance
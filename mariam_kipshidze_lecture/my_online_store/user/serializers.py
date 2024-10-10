from rest_framework import serializers

from user.models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'password', 'email']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

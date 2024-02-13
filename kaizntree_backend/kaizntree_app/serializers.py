from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import User


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "user_id", "SKU", "name", "category", "tags", "cost", "in_stock", "available_stock",
                  "minimum_stock", "desired_stock", "is_assembly", "is_component", "is_purchaseable", "is_sellable",
                  "is_bundle", "updated", "created"]
        read_only_fields = ('id', 'updated', 'created')
        extra_kwargs = {'user_id': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

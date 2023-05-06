from rest_framework import serializers
from .models import User, Friendship, FriendRequest


class UserSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели User
    """

    class Meta:
        model = User
        fields = ('id', 'username')


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели FriendRequest
    """

    class Meta:
        model = FriendRequest
        fields = ('id', 'sender', 'recipient')


class FriendshipSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Friendship
    """

    class Meta:
        model = Friendship
        fields = ('user1', 'user2')

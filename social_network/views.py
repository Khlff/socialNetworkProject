import json

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, Friendship, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer, \
    FriendshipSerializer


@api_view(['POST'])
def create_user(request) -> Response:
    """
    Зарегистрировать нового пользователя
    :return: код ответа: 201 - SUCCESSFUL_CREATED, 400 - BAD_REQUEST
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_friend_request(request, user_id: int) -> Response:
    """
    Отправить одному пользователю заявку в друзья другому.
    Если юзер, который отправляет заявку в друзья уже имеет входящую заявку
    от получателя, то они автоматически добавятся в друзья
    :param request: WSGI запрос
    :param user_id: id от кого отправить заявку
    :return: код ответа: 201 - SUCCESSFUL_CREATED
    """
    sender = User.objects.get(id=user_id)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    recipient_id = body.get('recipientId', None)
    recipient = User.objects.get(id=recipient_id)

    friend_request = FriendRequest.objects.filter(sender=recipient,
                                                  recipient=sender).first()

    if friend_request:
        friendship = Friendship.objects.create(user1=sender, user2=recipient)

        friend_request = FriendRequest.objects.get(
            recipient=user_id,
            sender=recipient_id
        )
        friend_request.delete()

        return Response(FriendshipSerializer(friendship).data,
                        status=status.HTTP_201_CREATED)
    else:
        friend_request = FriendRequest.objects.create(sender=sender,
                                                      recipient=recipient)
        return Response(FriendRequestSerializer(friend_request).data,
                        status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def accept_reject_friend_request(request, user_id: int) -> Response:
    """
    Принять/отклонить пользователю заявку в друзья от другого пользователя.
    :param request: WSGI запрос
    :param user_id: id у которого принять/отменить заявку
    :return: Код ответа: 200 - OK
    """
    user = User.objects.get(id=user_id)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    sender_id = body.get('senderId', None)
    request_status = body.get('status', None)

    friend_request = FriendRequest.objects.get(
        recipient=user,
        sender=User.objects.get(id=sender_id)
    )
    if request_status == 'accepted':
        Friendship.objects.create(user1=user, user2=friend_request.sender)
    friend_request.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def list_friend_requests(request, user_id: int) -> Response:
    """
    Посмотреть список исходящих и входящих заявок в друзья пользователя
    :param request: WSGI запрос
    :param user_id: у кого смотрим
    :return: dict {received: входящие заявки дружбы, sent: исходящие}
    """
    user = User.objects.get(id=user_id)
    received_requests = FriendRequest.objects.filter(recipient=user)
    sent_requests = FriendRequest.objects.filter(sender=user)
    return Response({
        'received': FriendRequestSerializer(received_requests, many=True).data,
        'sent': FriendRequestSerializer(sent_requests, many=True).data
    })


@api_view(['GET'])
def list_friends(request, user_id: int) -> Response:
    """
    Получить список друзей пользователя
    @param request: WSGI запрос
    @param user_id: у кого смотрим
    @return: Response object containing friends list
    """
    user = get_object_or_404(User, id=user_id)
    friendships = Friendship.objects.filter(user1=user) | Friendship.objects. \
        filter(user2=user)
    friends_list = []
    for friendship in friendships:
        if friendship.user1 == user:
            friend = friendship.user2
        else:
            friend = friendship.user1
        friend_data = {'id': friend.id, 'username': friend.username}
        friends_list.append(friend_data)
    return Response({'friends': friends_list})


@api_view(['GET'])
def get_friend_status(request, user_id: int) -> Response:
    """
    Получить статус дружбы пользователя с другим пользователем
    @param request: WSGI запрос
    @param user_id: id первого пользователя, у которого смотрим
    @return: True - друзья, False - нет
    """
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    friend_id = body.get('friendId', None)

    user = User.objects.get(id=user_id)
    friend = User.objects.get(id=friend_id)
    friendship1 = Friendship.objects.filter(user1=user, user2=friend)
    friendship2 = Friendship.objects.filter(user1=friend, user2=user)
    return Response({
        'status': bool(friendship1 or friendship2)
    })


@api_view(['DELETE'])
def remove_from_friends(request, user_id: int, friend_id: int) -> Response:
    """
    Удалить из списка друзей
    @param request: WSGI запрос
    @param user_id: id у кого удаляем
    @param friend_id: id который удаляем
    @return: HTTP response 200, если успешно удалилось
    """
    user = User.objects.get(id=user_id)
    friend = User.objects.get(id=friend_id)
    Friendship.objects.filter(
        Q(user1=user, user2=friend) | Q(user1=friend, user2=user)).delete()
    return Response({'ok'}, status=status.HTTP_200_OK)

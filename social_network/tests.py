import json
from collections import OrderedDict

from django.http import JsonResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from social_network.models import User, Friendship, FriendRequest


class SocialNetworkTestCase(APITestCase):
    def setUp(self):
        self.first_test_user = User.objects.create(username='test', id=1111)
        self.second_test_user = User.objects.create(username='test2', id=2222)

    def test_adding_new_user(self):
        response = self.client.post(
            reverse('new_user'), data={"username": "Nikita", "id": 23123},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {'id': 23123, 'username': 'Nikita'})

    def test_that_user_exists(self):
        response = self.client.post(reverse('new_user'), data={
            "username": "Ivan", "id": 1111}, format='json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'id':
                [
                    ErrorDetail(string='user с таким id уже существует.',
                                code='unique'
                                )
                ]}
        )

    def test_send_friend_request(self):
        response = self.client.post(
            reverse('friend_request', kwargs={"user_id": 1111}),
            json.dumps({"recipientId": 2222}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {'id': 1, 'sender': 1111, 'recipient': 2222})

    def test_auto_accept(self):
        test_friend_request = FriendRequest.objects.create(
            sender=self.first_test_user,
            recipient=self.second_test_user)

        response = self.client.post(
            reverse('friend_request', kwargs={"user_id": 2222}),
            json.dumps({"recipientId": 1111}), content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {'user1': 2222, 'user2': 1111})

    def test_accept_request(self):
        test_friend_request = FriendRequest.objects.create(
            sender=self.first_test_user,
            recipient=self.second_test_user)

        response = self.client.put(
            reverse('arequest', kwargs={"user_id": 2222}),
            json.dumps({"senderId": 1111, "status": "accepted"}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_requests_list(self):
        third_test_user = User.objects.create(username='test', id=3333)
        first_test_friend_request = FriendRequest.objects.create(
            sender=self.first_test_user,
            recipient=self.second_test_user)

        second_test_friend_request = FriendRequest.objects.create(
            sender=self.second_test_user,
            recipient=third_test_user)

        response = self.client.get(
            reverse('requests', kwargs={"user_id": 2222})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {
                'received': [
                    OrderedDict([('id', 1),
                                 ('sender', 1111),
                                 ('recipient', 2222)])
                ],
                'sent': [
                    OrderedDict([('id', 2),
                                 ('sender', 2222),
                                 ('recipient', 3333)])
                ]
            }
        )

    def test_get_friends(self):
        Friendship.objects.create(user1=self.first_test_user,
                                  user2=self.second_test_user)

        response = self.client.get(
            reverse('friends', kwargs={"user_id": 1111})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'friends': [{'id': 2222, 'username': 'test2'}]})

    def test_get_successful_friend_status(self):
        Friendship.objects.create(user1=self.first_test_user,
                                  user2=self.second_test_user)

        response = self.client.get(
            reverse('friend_status', kwargs={"user_id": 1111}),
            {"friendId": 2222},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'status': True})

    def test_delete_friend(self):
        Friendship.objects.create(user1=self.first_test_user,
                                  user2=self.second_test_user)

        response = self.client.delete(
            reverse('friend_remove',
                    kwargs={"user_id": 1111, "friend_id": 2222})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'ok'})

    def test_unsuccessful_delete_friend(self):
        response = self.client.delete(
            reverse('friend_remove',
                    kwargs={"user_id": 1111, "friend_id": 3333})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='sent_requests')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='received_requests')


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='friends1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='friends2')

from . import views
from django.urls import path

urlpatterns = [
    path('user/', views.create_user, name='new_user'),
    path('user/<int:user_id>/request/', views.send_friend_request,
         name='friend_request'),
    path('user/<int:user_id>/arequest/', views.accept_reject_friend_request,
         name='arequest'),
    path('user/<int:user_id>/requests/', views.list_friend_requests,
         name='requests'),
    path('user/<int:user_id>/friends/', views.list_friends, name='friends'),
    path('user/<int:user_id>/friend/', views.get_friend_status,
         name='friend_status'),
    path('user/<int:user_id>/friend/<int:friend_id>/',
         views.remove_from_friends, name='friend_remove'),
]

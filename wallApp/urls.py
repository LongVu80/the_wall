from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('success/', views.success),
    path('logout', views.logout),
    path('message', views.message),
    path('comment', views.comment),
    path('deleteMessage/<int:message_id>', views.deleteMessage),
    path('deleteComment/<int:comment_id>', views.deleteComment),
]
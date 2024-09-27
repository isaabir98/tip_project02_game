from django.urls import path
from . import views


urlpatterns=[
    path('',views.user,name='user'),
    path('/start',views.index,name='index'),
    path('/category',views.category,name='category')
]
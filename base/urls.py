from django.urls import path
from . views import user,index,category,admin_login,login_view,create_user,game_view,game_panel

urlpatterns = [
    path('', user, name='user'),                  
    path('start', index, name='index'),             
    path('category', category, name='category'),    
    path('login/now/', admin_login, name='admin_login'),
    path('login/', login_view, name='login'), 
    path('create-user/', create_user, name='create_user'),
    path('game_view/', game_view, name='game_view'),
    path('game_panel/<str:game_type>/',game_panel, name='game_panel'),
]

from django.urls import path
from . import views


urlpatterns=[
    path('',views.user,name='user'),
    path('/start',views.index,name='index'),
    path('/category',views.category,name='category'),
    path('admin/login/', views.admin_login, name='admin_login'),
    # path('admin/panel/', your_admin_panel_view, name='admin_panel'),
]
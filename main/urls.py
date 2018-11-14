from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('register/', views.register_view, name='register_view'),
    path('login_check/', views.username_check, name='username_check'),
    path('', views.index_view, name='index_view'),
    path('search', views.search, name='search'),
    path('account', views.account_view, name='account_view'),
    path('account/password_change/', views.password_change, name='password_change'),
    path('account/delete/', views.delete_account, name='delete_account'),
    path('account/set_timezone/', views.set_account_timezone, name='set_account_timezone')
]
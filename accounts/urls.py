from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name= 'login'),
    path('logout/', views.logoutuser, name='logout'),

    path('', views.home, name='home'),
    path('users/', views.userpage, name='users-page'),
    path('account/', views.accountSettings, name='account'),
    path('products/',views.product, name='products'),
    path('customer/<str:pk_test>/',views.customer, name='customer'),

    path('create_order/<str:pk>/', views.createorder, name='create_order'),
    path('update_order/<str:pk>/', views.UpdateOrder, name='update_order'),
    path('delete_order/<str:pk>/',views.deleteorder,name='delete_order')
]

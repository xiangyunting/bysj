from django.urls import path

from Doctor import views

urlpatterns = [
    path('', views.LoginRedirect.as_view()),
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('checkuname/', views.CheckUname.as_view()),
    path('operate/', views.OperateView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('loadCode.jpg', views.LoadCodeView.as_view()),
    path('checkcode/', views.CheckCodeView.as_view()),
]
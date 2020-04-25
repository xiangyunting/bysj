
from django.urls import path, re_path

from Donor import views
from bysj.settings import MEDIA_ROOT

urlpatterns = [

    path('checkuserid/', views.CheckUserId),
    path('checkbloodid/', views.CheckBloodId),

    path('adddonor/', views.AddDonorView.as_view()),
    path('adddonor/<str:donorid>/', views.AddDonorView.as_view()),
    path('changedonor/', views.ChangeDonor.as_view()),
    path('changedonor/<str:donorid>/', views.ChangeDonor.as_view()),
    path('checkdonor/', views.CheckDonor.as_view()),
    path('checkdonor/<int:num>/', views.CheckDonor.as_view()),

    path('deletedonor/<str:donorid>/', views.DeleteDonor.as_view()),
    path('deletedonor/<int:num>/<str:donorid>/', views.DeleteDonor.as_view()),

    path('addblood/', views.AddBlood.as_view()),
    path('addblood/<str:donorid>/', views.AddBlood.as_view()),
    path('changedonor/<str:donorid>/', views.ChangeDonor.as_view()),
    path('checkblood/', views.CheckBlood.as_view()),
    path('checkblood/<int:num>/', views.CheckBlood.as_view()),

    path('changeblood/', views.ChangeBlood.as_view()),
    path('changeblood/<int:bloodid>/', views.ChangeBlood.as_view()),

    path('deleteblood/<int:bloodid>/', views.DeleteBlood.as_view()),
    path('deleteblood/<int:num>/<int:bloodid>/', views.DeleteBlood.as_view()),
]

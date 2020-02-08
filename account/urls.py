from django.urls import path
from account import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.SignupView.as_view(), name="signup_init"),
    path('signup/done/', views.SignupDoneView.as_view(), name="signup_done"),
    path('signup/complete/<token>/',
         views.SignupCompleteView.as_view(), name="signup_complete"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('option/', views.OptionView.as_view(), name="option"),
]

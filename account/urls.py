from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path('login/', views.LoginView.as_view(),name="login"),
    path('signup/', views.SignupView.as_view(),name="signup_init"),
    path('signup/done/', views.SignupDoneView.as_view(),name="signup_done"),
    path('signup/complete/<token>/', views.SignupCompleteView.as_view(),name="signup_complete"),
]

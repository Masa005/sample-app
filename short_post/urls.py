from django.urls import path
from short_post import views

app_name = 'short_post'

urlpatterns = [
    path('home/', views.HomeView.as_view(),name="home"),
    path('timeline/', views.TimeLineView.as_view(),name="timeline"),
]

from django.urls import path
from sample_app import views

app_name = 'sample_app'

urlpatterns = [
    path('', views.init,name='init'),
    path('error/', views.ErrorView.as_view(),name='error'),
]

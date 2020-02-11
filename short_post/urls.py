from django.urls import path
from short_post import views

app_name = 'short_post'

urlpatterns = [
    path('home/', views.HomeView.as_view(), name="home"),
    path('timeline/', views.TimeLineView.as_view(), name="timeline"),
    path('post_load/', views.post_load_api, name="post_load"),
    path('favorite_add/', views.favorite_add_api, name="favorite_add"),
    path('favorite_delete/', views.favorite_delete_api,
         name="favorite_delete"),
    path('fav_load/', views.fav_load_api, name="fav_load"),
]

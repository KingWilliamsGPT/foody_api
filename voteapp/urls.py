from django.urls import path

from . import views

app_name = "voteapp" # app namespace

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('<int:poll_id>/', views.PollDetail.as_view(), name="poll_detail"),
]

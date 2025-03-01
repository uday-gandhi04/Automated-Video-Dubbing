# dubbing/urls.py

from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.video_upload, name='video_upload'),
    path('upload/', views.video_upload, name='video_upload'),  # URL for video upload
    path('download/<str:filename>/', views.video_download, name='video_download'),  # URL for video download
]

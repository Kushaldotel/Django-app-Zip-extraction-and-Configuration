from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    # Add more URLs for your app here
]

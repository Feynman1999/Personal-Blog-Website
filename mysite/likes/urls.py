from .views import * 
from django.urls import path

# start with /likes/
urlpatterns = [
    path('like_change', like_change , name='like_change'),
]

from .views import * 
from django.urls import path

# start with /user/
urlpatterns = [
    path('login/', login, name='login'),
    path('login_for_modal/', login_for_modal, name='login_for_modal'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('user_info/', user_info, name='user_info'),
]



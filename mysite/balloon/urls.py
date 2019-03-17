from .views import * 
from django.urls import path

# start with /balloon/
urlpatterns = [
    path('', balloon_board , name='balloon_board'),
    path('change_status', change_status, name="change_status"),
    path('set_para', set_para, name="set_para"),
]

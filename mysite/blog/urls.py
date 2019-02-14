from .views import * 
from django.urls import path

# start with /blog/
urlpatterns = [
    path('', article_list, name='article_list'),
    path('<int:article_id>', article_detail, name='article_detail'),
    path('type/<int:type_id>', article_list_with_type , name='article_list_with_type'),
    path('date/<int:year>/<int:month>', article_list_with_date, name='article_list_with_date'),
]

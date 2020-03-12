from django.urls import path
from . import views
urlpatterns = [
    path('index', views.index, name='index'),
    path('show/', views.showMoudles(request='GET'), name='show'),
]

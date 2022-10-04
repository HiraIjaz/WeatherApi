from django.urls import path

from . import views

urlpatterns = [
    path('<slug:message>/', views.index),
    path('info/<slug:scode>/', views.getweatherinfo)
]



from django.urls import path

from . import views

urlpatterns = [
    path('<slug:message>/', views.sampleResponse),
    path('info/<slug:scode>/', views.getWeatherInfo)
]

from django.urls import path
from .views import *

urlpatterns = [
    path('trains/', ListTrainView.as_view()),
    path('trains/create/', CreateTrainView.as_view()),
    path('trains/update/<int:pk>/', UpdateTrainView.as_view()),
    path('trains/search/', SearchTrainView.as_view()),
]
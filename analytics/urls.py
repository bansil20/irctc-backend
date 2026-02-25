from django.urls import path
from .views import *

urlpatterns = [
    path('analytics/top-routes/', TopRoutesAnalyticsView.as_view()),
]
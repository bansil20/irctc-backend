from django.urls import path
from .views import *

urlpatterns = [
    path('bookings/', CreateBookingView.as_view()),
    path('bookings/my/', MyBookingsView.as_view()),

]
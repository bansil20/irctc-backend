from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction

from .models import Booking
from .serializers import BookingCreateSerializer, BookingDetailSerializer
from trains.models import Train


# Create your views here.

class CreateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic #ensure everything inside is save or nopthing
    def post(self, request):

        # Validate request data using serializer
        serializer = BookingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        train = serializer.validated_data["train"]
        seats_requested = serializer.validated_data["seats_booked"]

        # train info
        train = Train.objects.select_for_update().get(id=train.id)

        # Check seat availability
        if train.available_seats < seats_requested:
            return Response(
                {"error": "Not enough seats available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Deduct seats
        train.available_seats -= seats_requested
        train.save()

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            train=train,
            seats_booked=seats_requested
        )

        return Response(
            BookingDetailSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )
    
    
class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user).select_related('train')
        serializer = BookingDetailSerializer(bookings, many=True)
        return Response(serializer.data)    
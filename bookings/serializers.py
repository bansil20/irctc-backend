from rest_framework import serializers
from .models import Booking
from trains.models import Train
from trains.serializers import TrainSerializer


# Used for POST (create booking)
class BookingCreateSerializer(serializers.ModelSerializer):

    train = serializers.PrimaryKeyRelatedField(
        queryset=Train.objects.all()
    )

    def validate_seats_booked(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Seats must be greater than 0"
            )
        return value

    class Meta:
        model = Booking
        fields = ['train', 'seats_booked']


# Used for GET (/my)
class BookingDetailSerializer(serializers.ModelSerializer):

    train = TrainSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'train', 'seats_booked', 'booking_time']
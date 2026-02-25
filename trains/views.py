from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Train
from .serializers import TrainSerializer
from accounts.permissions import IsAdminRole

import time
from datetime import datetime, timezone
from analytics.mongo import api_logs_collection
# Create your views here.

# Create Train (Admin Only)
class CreateTrainView(APIView):
    permission_classes = [IsAdminRole]

    def post(self, request):
        serializer = TrainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Update Train (Admin Only)
class UpdateTrainView(APIView):
    permission_classes = [IsAdminRole]

    def put(self, request, pk):
        try:
            train = Train.objects.get(pk=pk)
        except Train.DoesNotExist:
            return Response(
                {"error": "Train not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TrainSerializer(train, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# View All Trains (Logged Users)
class ListTrainView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trains = Train.objects.all()
        serializer = TrainSerializer(trains, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Search Train + MongoDB Logging
class SearchTrainView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_time = time.time()

        source = request.query_params.get('source')
        destination = request.query_params.get('destination')
        date = request.query_params.get('date')

        if not source or not destination:
            return Response(
                {"error": "source and destination are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        trains = Train.objects.filter(
            source__iexact=source,
            destination__iexact=destination
        )

        # Optional date filter
        if date:
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
                trains = trains.filter(departure_time__date=date_obj)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = TrainSerializer(trains, many=True)
        response_data = serializer.data

        end_time = time.time()
        execution_time = round((end_time - start_time) * 1000, 2)

        # Log to MongoDB
        api_logs_collection.insert_one({
            "endpoint": "/api/trains/search/",
            "user_id": request.user.id,
            "params": {
                "source": source,
                "destination": destination,
                "date": date
            },
            "execution_time_ms": execution_time,
            "timestamp": datetime.now(timezone.utc)
        })

        return Response(response_data, status=status.HTTP_200_OK)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from analytics.mongo import api_logs_collection

# Create your views here.

class TopRoutesAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        pipeline = [
            {
                "$match": {
                    "endpoint": "/api/trains/search/"
                }
            },
            {
                "$group": {
                    "_id": {
                        "source": "$params.source",
                        "destination": "$params.destination"
                    },
                    "search_count": {"$sum": 1}
                }
            },
            {
                "$sort": {"search_count": -1}
            },
            {
                "$limit": 5
            }
        ]

        results = list(api_logs_collection.aggregate(pipeline))

        if not results:
            return Response({
                "message": "No searches have been performed yet."
            })

        formatted_results = [
            {
                "source": item["_id"]["source"],
                "destination": item["_id"]["destination"],
                "search_count": item["search_count"]
            }
            for item in results
        ]

        return Response(formatted_results)
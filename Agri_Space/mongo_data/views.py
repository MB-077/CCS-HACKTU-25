from rest_framework.views import APIView
from rest_framework.response import Response
from mongo_data.mongo_models import SensorDataDoc
import mongoengine
from datetime import datetime

class SensorHumidityTempView(APIView):
    def get(self, request, format=None):
        sensor_docs = SensorDataDoc.objects.only("dht11_humidity", "dht11_temperature", "timestamp")
        data = []
        for doc in sensor_docs:
            data.append({
                "timestamp": doc.timestamp.isoformat(),
                "humidity": doc.dht11_humidity,
                "temperature": doc.dht11_temperature,
            })
        return Response(data)

class SensorFlowView(APIView):
    def get(self, request, format=None):
        sensor_docs = SensorDataDoc.objects.only("flow_rate", "flow", "timestamp")
        data = []
        for doc in sensor_docs:
            data.append({
                "timestamp": doc.timestamp.isoformat(),
                "flow_rate": doc.flow_rate,
                "flow": doc.flow,
            })
        return Response(data)

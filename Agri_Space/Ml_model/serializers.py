from rest_framework import serializers

class Crop_Recommendation_Serializer(serializers.Serializer):
    N = serializers.FloatField()
    P = serializers.FloatField()
    K = serializers.FloatField()
    temperature = serializers.FloatField()
    humidity = serializers.FloatField()
    ph = serializers.FloatField()
    rainfall = serializers.FloatField()

class Fertilizer_Prediction_Serializer(serializers.Serializer):
    Temperature = serializers.FloatField()
    Humidity = serializers.FloatField()
    Moisture = serializers.FloatField()
    Soil_Type = serializers.CharField()
    Crop_Type = serializers.CharField()
    Nitrogen = serializers.FloatField()
    Potassium = serializers.FloatField()
    Phosphorous = serializers.FloatField()
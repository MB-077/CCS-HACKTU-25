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

class Yield_Prediction_Serializer(serializers.Serializer):
    Crop = serializers.CharField()
    Crop_Year = serializers.IntegerField()
    Season = serializers.CharField()
    State = serializers.CharField()
    Area = serializers.FloatField()
    Annual_Rainfall = serializers.FloatField()
    Fertilizer = serializers.FloatField()
    Pesticide = serializers.FloatField()
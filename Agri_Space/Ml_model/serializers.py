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

class Irrigation_Prediction_Serilizer(serializers.Serializer):
    CropType = serializers.CharField()
    CropDays = serializers.IntegerField()
    temperature = serializers.FloatField()
    Humidity = serializers.FloatField()
    SoilMoisturePer = serializers.FloatField()


class Optimal_RGB_Serializer(serializers.Serializer):
    R = serializers.FloatField()
    G = serializers.FloatField()
    B = serializers.FloatField()
    Crop_Type = serializers.CharField()
    Temperature = serializers.FloatField()
    Humidity = serializers.FloatField()
    PPFD = serializers.FloatField()
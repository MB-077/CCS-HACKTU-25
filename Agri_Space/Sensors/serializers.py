from rest_framework import serializers
from .models import *

class IrrigationCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrrigationCycle
        fields = ['start_time', 'duration']


class RelayStateSerializer(serializers.ModelSerializer):
    cycles = IrrigationCycleSerializer(many=True)
    
    class Meta:
        model = RelayState
        fields = ['state', 'day_of_week', 'cycles']

    def create(self, validated_data):
        cycles_data = validated_data.pop('cycles')
        relay_state = RelayState.objects.create(**validated_data)
        for cycle_data in cycles_data:
            IrrigationCycle.objects.create(relay_state=relay_state, **cycle_data)
        return relay_state
    

class WaterConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterConsumption
        fields = '__all__'
        

class TotalWaterUsageSerializer(serializers.Serializer):
    
    class Meta:
        model = TotalWaterUsage
        fields = '__all__'
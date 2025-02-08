from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from datetime import datetime


@api_view(['GET', 'POST'])
def relay_control(request):
    if request.method == 'POST':
        serializer = RelayStateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        now = datetime.now()
        today = now.strftime('%A')
        current_time = now.time()

        relay_state = RelayState.objects.filter(day_of_week=today).last()
        if relay_state:
            cycles = relay_state.cycles.all()
            for cycle in cycles:
                start_time = cycle.start_time
                end_time = (datetime.combine(datetime.today(), start_time) + cycle.duration).time()

                if start_time <= current_time <= end_time:
                    remaining_runtime = (datetime.combine(datetime.today(), end_time) - now).total_seconds()

                    response_data = {
                        "relay_state": "ON",
                        "runtime": int(remaining_runtime) 
                    }
                    return Response(response_data, status=status.HTTP_200_OK)

        return Response({"relay_state": "OFF", "runtime": 0}, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def relay_state(request, id):
    try:
        relay_state = RelayState.objects.get(pk=id)
    except RelayState.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RelayStateSerializer(relay_state)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT' or request.method == 'PATCH':
        partial = request.method == 'PATCH'
        serializer = RelayStateSerializer(relay_state, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        relay_state.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def irrigation_cycle(request, id):
    try:
        irrigation_cycle = IrrigationCycle.objects.get(pk=id)
    except IrrigationCycle.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IrrigationCycleSerializer(irrigation_cycle)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT' or request.method == 'PATCH':
        partial = request.method == 'PATCH'
        serializer = IrrigationCycleSerializer(irrigation_cycle, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        irrigation_cycle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def water_usage(request):
    if request.method == 'GET':
        water_consumption = WaterConsumption.objects.all()
        serializer = WaterConsumptionSerializer(water_consumption, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def total_water_usage(request):
    if request.method == 'GET':
        total_water_usage = TotalWaterUsage.objects.get(id=1)
        serializer = TotalWaterUsageSerializer(total_water_usage)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
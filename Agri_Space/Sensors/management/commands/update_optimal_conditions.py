from django.core.management.base import BaseCommand
from Sensors.models import SensorData, CropsOptimalConditions, ChildNodeSensorData
from Users.models import UserImportantDetails, UserStatus
from Users.models import StateData
from Ml_model.views import predict_optimal_conditions_for_input
from Ml_model.views import pkl_models, label_encoders
from datetime import datetime
from Ml_model.utils import get_bbch_stage
import joblib

active_users = UserStatus.objects.filter(online_status=True)

BBCH_FILE_PATH = "Ml_model/csv_files/crop_growth_stages_fixed_5.csv"

targets = ['temperature', 'humidity', 'soil_moisture', 'solar_intensity', 'pressure']

class Command(BaseCommand):
    help = "Update crop optimal conditions based on unprocessed sensor readings."
        
    def handle(self, *args, **kwargs):
        
        try:
            active_user_status = UserStatus.objects.filter(online_status=True).first()
            if not active_user_status:
                self.stdout.write(self.style.ERROR("No active user found."))
                return

            active_user = active_user_status.user
            user_details = UserImportantDetails.objects.filter(user=active_user).first()
            if not user_details:
                self.stdout.write(self.style.ERROR("User details not found."))
                return

            user = user_details.user
            crop_grown = user_details.crop_grown
            
            bbch_stage = self.getgrowth_stage(user_details, crop_grown)
            growth_stage = self.get_major_growth_stage(bbch_stage)
            
            
            soil_type = self.get_soil_type(user_details.state)
            rainfall = self.get_rainfall(user_details.state)
            
            try:
                encoded_crop_type = label_encoders['crop_type'].fit_transform([crop_grown])[0]
                encoded_growth_stage = label_encoders['growth_stage'].fit_transform([growth_stage])[0]
                encoded_state = label_encoders['state'].fit_transform([user_details.state])[0]
                encoded_soil_type = label_encoders['soil_type'].fit_transform([soil_type])[0]
            except Exception as e:
                self.stderr.write(f"Error during label encoding: {str(e)}")
                return
            
            sensor_reading = SensorData.objects.all().last()
            child_node_sensor_reading = ChildNodeSensorData.objects.all().last()
            
            if sensor_reading and child_node_sensor_reading:
                sensor_data = {
                    "crop_type": encoded_crop_type,
                    "growth_stage": encoded_growth_stage,
                    "state": encoded_state,
                    "soil_type": encoded_soil_type,
                    "temperature": sensor_reading.dht11_temperature,
                    "humidity": sensor_reading.dht11_humidity,
                    "pressure": sensor_reading.atm_pressure,
                    "solar_intensity": sensor_reading.lux,
                    "soil_moisture": sensor_reading.soil_moisture_percent_1,
                    "rainfall": rainfall,
                    "soil_temperature": child_node_sensor_reading.node_DS18B20_temperature,
                }

                try:
                    predictions = predict_optimal_conditions_for_input(pkl_models, sensor_data)
                    print(f"Predictions: {predictions}")
                except Exception as e:
                    self.stderr.write(f"Error processing Sensor Data {sensor_reading.id}: {e}")
                    return
                
                optimal_data = {
                    "optimal_temperature_lower_bound": predictions.get("Optimal_Temp_Range_(°C)", [0, 0])[0],
                    "optimal_temperature_upper_bound": predictions.get("Optimal_Temp_Range_(°C)", [0, 0])[1],
                    "optimal_humidity_lower_bound": predictions.get("Optimal_Humidity_Range_(%)", [0, 0])[0],
                    "optimal_humidity_upper_bound": predictions.get("Optimal_Humidity_Range_(%)", [0, 0])[1],
                    "optimal_soil_moisture_percentage_lower_bound":  predictions.get("Optimal_Soil_Moisture_Range_(%)", [0, 0])[0],
                    "optimal_soil_moisture_percentage_upper_bound": predictions.get("Optimal_Soil_Moisture_Range_(%)", [0, 0])[1],
                    "optimal_lux_lower_bound": predictions.get("Optimal_Solar_Intensity_(W/m^2)", [0, 0])[0],
                    "optimal_lux_upper_bound": predictions.get("Optimal_Solar_Intensity_(W/m^2)", [0, 0])[1],
                }
                
                print(f"Optimal Data: {optimal_data}")

                CropsOptimalConditions.objects.update_or_create(
                    user = user,
                    crop_name=crop_grown,
                    defaults=optimal_data
                )

                self.stdout.write(self.style.SUCCESS(f"Processed Sensor Data {sensor_reading.id}"))
                
        except :
            self.stdout.write(self.style.ERROR("User details not found"))
            
    def getgrowth_stage(self, user_details, crop_grown):
        days_since_planting = (datetime.now().date() - user_details.planting_date).days
        bbch_stage = get_bbch_stage(BBCH_FILE_PATH, crop_grown, days_since_planting)
        return bbch_stage['Principal Stage']

    def get_major_growth_stage(self, bbch_stage):
        stage = bbch_stage.lower()

        if any(kw in stage for kw in ['germination', 'sprouting', 'bud development']):
            return 'Germination'
        
        elif any(kw in stage for kw in ['leaf development', 'rosette', 'tillering', 'side shoot', 'branch', 'stem elongation']):
            return 'Vegetative'
        
        elif any(kw in stage for kw in ['inflorescence', 'heading', 'flowering', 'anthesis']):
            return 'Flowering'
        
        elif any(kw in stage for kw in ['fruit', 'seed', 'tuber formation', 'ripening', 'maturity', 'berry']):
            return 'Maturation'
        
        elif any(kw in stage for kw in ['senescence', 'dormancy']):
            return 'Harvest'
        
        else:
            return 'Unknown'
        
    def get_soil_type(self, state):
        state_data = StateData.objects.filter(indian_state=state).last()
        if state_data:
            return state_data.soil_type
        return None
    
    def get_rainfall(self, state):
        state_data = StateData.objects.filter(indian_state=state).last()
        if state_data:
            return state_data.avg_monthly_rainfall
        return None
        
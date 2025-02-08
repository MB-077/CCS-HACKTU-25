# Django & DRF Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Third-party Libraries
import joblib
import pandas as pd
from sklearn.exceptions import NotFittedError

# Local Imports
from .serializers import (
    Crop_Recommendation_Serializer, 
    Fertilizer_Prediction_Serializer, 
    Yield_Prediction_Serializer,
)

# Create your views here.
class Crop_Recommendation(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model, self.scaler = self.load_model()

    @staticmethod
    def load_model():
        """Load the ML model and scaler with error handling."""
        model_path = 'Ml_model/trained_data/crop_recommendation/crop_recommendation_model.pkl'
        scaler_path = 'Ml_model/trained_data/crop_recommendation/crop_recommendation_scaler.pkl'
        try:
            return joblib.load(model_path), joblib.load(scaler_path)
        except FileNotFoundError:
            return None, None
        except Exception:
            return None, None

    def post(self, request, *args, **kwargs):
        if self.model is None or self.scaler is None:
            return Response(
                {"error": "Model or scaler could not be loaded. Please check the server configuration."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        serializer = Crop_Recommendation_Serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data_df = pd.DataFrame([serializer.validated_data])

        try:
            scaled_data = self.scaler.transform(data_df)
            prediction = self.model.predict(scaled_data)[0]
            return Response({"prediction": prediction}, status=status.HTTP_200_OK)
        except NotFittedError:
            return Response({"error": "Scaler is not properly trained."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except IndexError:
            return Response({"error": "Model did not return a prediction."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class Fertilizer_Prediction(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = self.load_model()

    @staticmethod
    def load_model():
        # Importing the Model
        model_path = 'Ml_model/trained_data/fertilizer_prediction/trained_model_fertilizer.pkl'
        
        try:
            return joblib.load(model_path)
        except FileNotFoundError:
            return None
        except Exception:
            return None

    def post(self, request, *args, **kwargs):

        if self.model is None:
            return Response(
                {"error": "Model could not be loaded. Please check the server configuration."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        serializer = Fertilizer_Prediction_Serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status==status.HTTP_400_BAD_REQUEST)
        
        data = pd.DataFrame([serializer.validated_data])
        try:
            prediction = self.fertilizer_model.predict(data)
            result = prediction[0]
            return Response({"prediction": result}, status=status.HTTP_200_OK)
        except IndexError:
            return Response({"error": "Model did not return a prediction."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class Yield_Prediction(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = self.load_model()

    @staticmethod
    def load_model():
        """Load the ML model with error handling."""
        model_path = 'Ml_model/trained_data/yield_prediction/yield_prediction_model.pkl'
        try:
            return joblib.load(model_path)
        except FileNotFoundError:
            return None
        except Exception:
            return None
        
    def post(self, request, *args, **kwargs):
        if self.model is None:
            return Response(
                {"error": "Model could not be loaded. Please check the server configuration."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        serializer = Yield_Prediction_Serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data_df = pd.DataFrame([serializer.validated_data])

        try:
            prediction = self.model.predict(data_df)[0] * data_df.at[0, "Area"]
            return Response({"prediction": prediction}, status=status.HTTP_200_OK)
        except IndexError:
            return Response({"error": "Model did not return a prediction."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
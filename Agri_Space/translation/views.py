from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Load IndicTrans2 Model
class TranslateTextView(APIView):
    permission_classes = [AllowAny]  # Allow requests from frontend

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_name = "ai4bharat/indictrans2-en-indic"
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def post(self, request, *args, **kwargs):
        text = request.data.get("text", "")
        target_lang = request.data.get("target_lang", "")

        if not text or not target_lang:
            return Response({"error": "Text and target_lang are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            inputs = self.tokenizer(text, return_tensors="pt")
            outputs = self.model.generate(**inputs, forced_bos_token_id=self.tokenizer.lang_code_to_id[target_lang])
            translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            return Response({"translated_text": translated_text}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

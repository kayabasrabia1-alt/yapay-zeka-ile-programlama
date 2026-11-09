import os
os.environ["GRPC_DNS_RESOLVER"] = "native"
import warnings
warnings.filterwarnings("ignore")
import google.generativeai as genai

API_KEY = "AQ.Ab8RN6L7Ne_RPmcHxm8z5Ukjs2c0jM3OSI0g5ETro6HLxBJY1Q"
genai.configure(api_key=API_KEY)

print("Hesabındaki kullanılabilir modeller listeleniyor...\n")
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print("Kullanılabilir Model:", model.name)
except Exception as e:
    print("Hata:", str(e))
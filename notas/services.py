import joblib, os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "modelo_notas.pkl")
_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

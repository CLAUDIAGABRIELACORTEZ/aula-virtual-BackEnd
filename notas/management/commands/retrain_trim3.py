from django.core.management.base import BaseCommand
from django.conf import settings
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd
import os
import joblib

from notas.models import HistoricoNota

# Ruta donde se guardará el modelo entrenado
MODEL_PATH = os.path.join(settings.BASE_DIR, "modelo_notas.pkl")

class Command(BaseCommand):
    help = "Entrena el modelo predictivo de nota del 3er trimestre a partir del histórico."

    def handle(self, *args, **options):
        # 1. Obtener datos históricos
        historial = HistoricoNota.objects.all()

        if historial.count() < 30:
            self.stderr.write(self.style.ERROR("❌ Se necesitan al menos 30 registros para entrenar el modelo."))
            return

        # 2. Convertir a DataFrame
        rows = []
        for h in historial:
            if None not in (h.nota_trim1, h.nota_trim2, h.nota_trim3):
                rows.append({
                    "trim1": h.nota_trim1,
                    "trim2": h.nota_trim2,
                    "trim3": h.nota_trim3,
                })

        df = pd.DataFrame(rows)

        if df.shape[0] < 30:
            self.stderr.write(self.style.ERROR("❌ Después de filtrar, hay menos de 30 filas con notas completas."))
            return

        # 3. Separar features y target
        X = df[["trim1", "trim2"]]
        y = df["trim3"]

        # 4. Dividir en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        # 5. Entrenar el modelo
        model = LinearRegression()
        model.fit(X_train, y_train)

        # 6. Evaluar
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        self.stdout.write(self.style.SUCCESS(f"📊 MAE en conjunto de prueba: {mae:.2f}"))

        # 7. Guardar el modelo entrenado
        joblib.dump(model, MODEL_PATH)
        self.stdout.write(self.style.SUCCESS(f"✅ Modelo entrenado guardado en {MODEL_PATH}"))

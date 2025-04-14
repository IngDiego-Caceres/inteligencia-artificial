import pandas as pd
import numpy as np
import random

# Semilla para reproducibilidad
np.random.seed(42)

# Generamos 500 registros
n = 500

# Posibles valores
horas = list(range(5, 23))  # desde las 5am hasta las 10pm
dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
climas = ['Soleado', 'Lluvioso', 'Nublado']
eventos = ['Sí', 'No']
rutas = list(range(1, 6))  # 5 rutas

# Crear dataset
data = {
    'hora_dia': np.random.choice(horas, n),
    'dia_semana': np.random.choice(dias_semana, n),
    'clima': np.random.choice(climas, n),
    'eventos_especiales': np.random.choice(eventos, n, p=[0.2, 0.8]),  # 20% con eventos
    'ruta_id': np.random.choice(rutas, n),
}

df = pd.DataFrame(data)

# Simulamos el número de pasajeros como variable objetivo
def simular_pasajeros(row):
    base = random.randint(10, 30)
    if row['hora_dia'] in [7, 8, 17, 18]:  # Hora pico
        base += random.randint(20, 40)
    if row['dia_semana'] in ['Sábado', 'Domingo']:
        base -= random.randint(5, 15)
    if row['clima'] == 'Lluvioso':
        base += random.randint(5, 10)
    if row['eventos_especiales'] == 'Sí':
        base += random.randint(15, 25)
    return max(base, 0)

df['pasajeros'] = df.apply(simular_pasajeros, axis=1)

print(df.head())
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Variables categóricas
columnas_categoricas = ['dia_semana', 'clima', 'eventos_especiales']

# Separar X y y
X = df.drop('pasajeros', axis=1)
y = df['pasajeros']

# Transformador para variables categóricas
preprocesamiento = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), columnas_categoricas)
    ],
    remainder='passthrough'  # dejar las numéricas tal como están
)

# Pipeline con modelo de regresión lineal
modelo = Pipeline(steps=[
    ('preprocesamiento', preprocesamiento),
    ('regresion', LinearRegression())
])

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenar modelo
modelo.fit(X_train, y_train)

# Evaluar
y_pred = modelo.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Error cuadrático medio: {mse:.2f}")

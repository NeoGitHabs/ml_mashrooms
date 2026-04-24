import joblib
import numpy as np
import pandas as pd
import uvicorn
from columns import all_columns
from schema import MushroomsSchema
from fastapi import FastAPI
from pathlib import Path



BASE_DIR = Path(__file__).parent

model = joblib.load(BASE_DIR / 'model_rf.pkl')
scaler = joblib.load(BASE_DIR / 'scaler.pkl')


app = FastAPI()


@app.post('/predict')
async def predict(data: MushroomsSchema):
    # Преобразуем входные данные в DataFrame
    data_dict = data.model_dump(by_alias=True)
    input_data = pd.DataFrame([data_dict])

    # Обработка '?' в stalk-root
    input_data['stalk-root'] = input_data['stalk-root'].replace('?', np.nan)
    input_data['stalk-root'] = input_data['stalk-root'].fillna('b')  # Мода из предобработки

    # One-Hot Encoding
    input_encoded = pd.get_dummies(input_data)

    # Создаём DataFrame с нулями для всех ожидаемых столбцов
    zero_df = pd.DataFrame(0, index=[0], columns=all_columns)
    # Обновляем значения для существующих столбцов
    for col in input_encoded.columns:
        if col in all_columns:
            zero_df[col] = input_encoded[col]

    # Упорядочиваем столбцы
    input_encoded = zero_df[all_columns]

    # Преобразуем в numpy массив без имён столбцов
    input_array = input_encoded.to_numpy()

    # Предсказание
    prediction = model.predict(input_array)[0]
    proba = model.predict_proba(input_array)[0][1]  # Вероятность для класса 1 (poisonous)

    # Формируем ответ
    return {
        "poisonous": bool(prediction),  # 1 -> True, 0 -> False
        "probability": float(proba)
    }


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

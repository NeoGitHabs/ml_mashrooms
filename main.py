import joblib
import uvicorn
import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal


app = FastAPI()

model = joblib.load('model_rf.pkl')
scaler = joblib.load('scaler.pkl')


expected_columns = [
    'cap-shape_c', 'cap-shape_f', 'cap-shape_k', 'cap-shape_s', 'cap-shape_x',
    'cap-surface_g', 'cap-surface_s', 'cap-surface_y',
    'cap-color_c', 'cap-color_e', 'cap-color_g', 'cap-color_n', 'cap-color_p',
    'cap-color_r', 'cap-color_u', 'cap-color_w', 'cap-color_y',
    'bruises_t', 'odor_c', 'odor_f', 'odor_l', 'odor_m', 'odor_n', 'odor_p',
    'odor_s', 'odor_y', 'gill-attachment_f', 'gill-spacing_w', 'gill-size_n',
    'gill-color_e', 'gill-color_g', 'gill-color_h', 'gill-color_k', 'gill-color_n',
    'gill-color_o', 'gill-color_p', 'gill-color_r', 'gill-color_u', 'gill-color_w',
    'gill-color_y', 'stalk-shape_t', 'stalk-surface-above-ring_k',
    'stalk-surface-above-ring_s', 'stalk-surface-above-ring_y',
    'stalk-surface-below-ring_k', 'stalk-surface-below-ring_s',
    'stalk-surface-below-ring_y', 'stalk-color-above-ring_c',
    'stalk-color-above-ring_e', 'stalk-color-above-ring_g',
    'stalk-color-above-ring_n', 'stalk-color-above-ring_o',
    'stalk-color-above-ring_p', 'stalk-color-above-ring_w',
    'stalk-color-above-ring_y', 'stalk-color-below-ring_c',
    'stalk-color-below-ring_e', 'stalk-color-below-ring_g',
    'stalk-color-below-ring_n', 'stalk-color-below-ring_o',
    'stalk-color-below-ring_p', 'stalk-color-below-ring_w',
    'stalk-color-below-ring_y', 'veil-color_o', 'veil-color_w', 'veil-color_y',
    'ring-number_o', 'ring-number_t', 'ring-type_f', 'ring-type_l', 'ring-type_n',
    'ring-type_p', 'spore-print-color_h', 'spore-print-color_k',
    'spore-print-color_n', 'spore-print-color_o', 'spore-print-color_r',
    'spore-print-color_u', 'spore-print-color_w', 'spore-print-color_y',
    'population_c', 'population_n', 'population_s', 'population_v', 'population_y',
    'habitat_g', 'habitat_l', 'habitat_m', 'habitat_p', 'habitat_u', 'habitat_w'
]


class MushroomsSchema(BaseModel):
    cap_shape: Literal['b', 'c', 'x', 'f', 'k', 's'] = Field(..., alias='cap-shape')
    cap_surface: Literal['f', 'g', 'y', 's'] = Field(..., alias='cap-surface')
    cap_color: Literal['n', 'b', 'c', 'g', 'r', 'p', 'u', 'e', 'w', 'y'] = Field(..., alias='cap-color')
    bruises: Literal['t', 'f'] = Field(..., alias='bruises')
    odor: Literal['a', 'l', 'c', 'y', 'f', 'm', 'n', 'p', 's'] = Field(..., alias='odor')
    gill_attachment: Literal['a', 'd', 'f', 'n'] = Field(..., alias='gill-attachment')
    gill_spacing: Literal['c', 'w', 'd'] = Field(..., alias='gill-spacing')
    gill_size: Literal['b', 'n'] = Field(..., alias='gill-size')
    gill_color: Literal['k', 'n', 'b', 'h', 'g', 'r', 'o', 'p', 'u', 'e', 'w', 'y'] = Field(..., alias='gill-color')
    stalk_shape: Literal['e', 't'] = Field(..., alias='stalk-shape')
    stalk_root: Literal['b', 'c', 'u', 'e', 'z', 'r', '?'] = Field(..., alias='stalk-root')
    stalk_surface_above_ring: Literal['f', 'y', 'k', 's'] = Field(..., alias='stalk-surface-above-ring')
    stalk_surface_below_ring: Literal['f', 'y', 'k', 's'] = Field(..., alias='stalk-surface-below-ring')
    stalk_color_above_ring: Literal['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'] = Field(..., alias='stalk-color-above-ring')
    stalk_color_below_ring: Literal['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'] = Field(..., alias='stalk-color-below-ring')
    veil_type: Literal['p', 'u'] = Field(..., alias='veil-type')
    veil_color: Literal['n', 'o', 'w', 'y'] = Field(..., alias='veil-color')
    ring_number: Literal['n', 'o', 't'] = Field(..., alias='ring-number')
    ring_type: Literal['c', 'e', 'f', 'l', 'n', 'p', 's', 'z'] = Field(..., alias='ring-type')
    spore_print_color: Literal['k', 'n', 'b', 'h', 'r', 'o', 'u', 'w', 'y'] = Field(..., alias='spore-print-color')
    population: Literal['a', 'c', 'n', 's', 'v', 'y'] = Field(..., alias='population')
    habitat: Literal['g', 'l', 'm', 'p', 'u', 'w', 'd'] = Field(..., alias='habitat')

    class Config:
        populate_by_name = True


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
    zero_df = pd.DataFrame(0, index=[0], columns=expected_columns)
    # Обновляем значения для существующих столбцов
    for col in input_encoded.columns:
        if col in expected_columns:
            zero_df[col] = input_encoded[col]

    # Упорядочиваем столбцы
    input_encoded = zero_df[expected_columns]

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

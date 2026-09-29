from pathlib import Path

import streamlit as st
import pandas as pd
import joblib

papka = Path(__file__).resolve().parent / "models"
try:
    model_modul = joblib.load(papka / "model_modul.joblib")
    model_prochnost = joblib.load(papka / "model_prochnost.joblib")
    medians = joblib.load(papka / "medians.joblib")
except FileNotFoundError:
    st.error("Не найдены файлы моделей. Выполни исправленный ноутбук и сохрани папку models рядом с app.py.")
    st.stop()

polya = list(model_modul.feature_names_in_)

st.title("Прогноз свойств композита")
st.caption("Учебный прогноз. Полученные значения не заменяют испытания образца.")

znacheniya = {}
for col in polya:
    if col == "Угол нашивки, град":
        znacheniya[col] = st.selectbox(col, [0, 90], index=[0, 90].index(int(medians[col])))
    else:
        znacheniya[col] = st.number_input(col, value=float(medians[col]))

if st.button("Рассчитать"):
    # Нормировщики уже находятся внутри моделей, передаём исходные признаки.
    frame = pd.DataFrame([znacheniya], columns=polya)
    modul = float(model_modul.predict(frame)[0])
    prochnost = float(model_prochnost.predict(frame)[0])

    st.write("Модуль упругости при растяжении, ГПа:", round(modul, 3))
    st.write("Прочность при растяжении, МПа:", round(prochnost, 3))

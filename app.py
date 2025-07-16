import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Simulasi Spektrofotometer UV-Vis", layout="centered")

# ------------------ HEADER -------------------
st.title("🧪 Simulasi Spektrofotometer UV-Vis")
st.image("assets/spektro_uvvis.png", caption="Ilustrasi Instrumen UV-Vis", use_column_width=True)
st.markdown("""
Aplikasi ini mensimulasikan prinsip kerja spektrofotometer UV-Vis, seperti:
- Menentukan λ maks dari data spektrum
- Membuat kurva kalibrasi dari larutan standar
- Menentukan konsentrasi larutan sampel berdasarkan absorbansi
""")

# ------------------ MENU -------------------
menu = st.sidebar.radio("Pilih Simulasi", ["1. Spektrum λ maks", "2. Kurva Kalibrasi", "3. Konsentrasi Sampel"])

# ------------------ 1. SIMULASI SPEKTRUM -------------------
if menu == "1. Spektrum λ maks":
    st.subheader("1. Simulasi Penentuan λ Maks")

    # Data Spektrum Buatan
    wavelengths = np.arange(200, 801, 10)
    absorbances = np.exp(-((wavelengths - 500) ** 2) / (2 * 30**2)) + np.random.normal(0, 0.02, size=len(wavelengths))

    max_index = np.argmax(absorbances)
    lamda_max = wavelengths[max_index]

    fig, ax = plt.subplots()
    ax.plot(wavelengths, absorbances, label='Absorbansi')
    ax.axvline(lamda_max, color='red', linestyle='--', label=f'λ maks = {lamda_max} nm')
    ax.set_xlabel("Panjang Gelombang (nm)")
    ax.set_ylabel("Absorbansi")
    ax.legend()
    st.pyplot(fig)

    st.success(f"λ maks terletak pada **{lamda_max} nm**")

# ------------------ 2. KURVA KALIBRASI -------------------
elif menu == "2. Kurva Kalibrasi":
    st.subheader("2. Simulasi Kurva Kalibrasi")

    st.markdown("Masukkan data standar (konsentrasi dan absorbansi):")

    default_data = {
        "Konsentrasi (ppm)": [0, 5, 10, 15, 20, 25],
        "Absorbansi": [0.02, 0.13, 0.27, 0.40, 0.52, 0.64]
    }

    df = pd.DataFrame(default_data)
    edited_df = st.data_editor(df, use_container_width=True)

    X = np.array(edited_df["Konsentrasi (ppm)"]).reshape(-1, 1)
    y = np.array(edited_df["Absorbansi"])

    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_[0]
    
st.image("assets/spektro_uvvis.png", caption="Ilustrasi Instrumen UV-Vis", use_column_width=True)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Simulasi Spektrofotometer UV-Vis", layout="centered")

# ------------------ HEADER -------------------
st.title("🧪 Simulasi Spektrofotometer UV-Vis")
st.image("assets/spektrofotometer_uvvis_double_beam.webp", caption="Ilustrasi Instrumen UV-Vis")
st.markdown("""
Aplikasi ini mensimulasikan prinsip kerja spektrofotometer UV-Vis.  
Kamu dapat:
- Memasukkan data spektrum sendiri
- Membuat kurva kalibrasi dari data kamu
- Menghitung konsentrasi sampel berdasarkan nilai absorbansi
""")

# ------------------ MENU -------------------
menu = st.sidebar.radio("📋 Pilih Simulasi", ["1. Input Spektrum λ maks", "2. Input Kurva Kalibrasi", "3. Hitung Konsentrasi Sampel"])

# ------------------ 1. SPEKTRUM λ MAKS -------------------
if menu == "1. Input Spektrum λ maks":
    st.subheader("1. Simulasi Penentuan λ Maks dari Data Sendiri")

    st.markdown("Masukkan data panjang gelombang dan absorbansi secara manual atau dengan menyalin dari Excel (copy-paste):")

    input_df = st.text_area("Tempel data kamu di sini (format: λ,Absorbansi)", height=200,
                            placeholder="Contoh:\n200,0.01\n210,0.05\n220,0.15")

    if input_df:
        try:
            data = pd.read_csv(pd.compat.StringIO(input_df), header=None, names=["λ (nm)", "Absorbansi"])
            max_idx = data["Absorbansi"].idxmax()
            lambda_max = data.loc[max_idx, "λ (nm)"]

            st.success(f"λ maks dari data kamu adalah **{lambda_max} nm**")

            fig, ax = plt.subplots()
            ax.plot(data["λ (nm)"], data["Absorbansi"], marker='o')
            ax.axvline(lambda_max, color='red', linestyle='--', label=f'λ maks = {lambda_max} nm')
            ax.set_xlabel("Panjang Gelombang (nm)")
            ax.set_ylabel("Absorbansi")
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# ------------------ 2. KURVA KALIBRASI -------------------
elif menu == "2. Input Kurva Kalibrasi":
    st.subheader("2. Kurva Kalibrasi (Input Manual)")

    st.markdown("Masukkan data konsentrasi dan absorbansi standar:")

    default_data = {
        "Konsentrasi (ppm)": [0, 5, 10, 15, 20],
        "Absorbansi": [0.01, 0.12, 0.23, 0.35, 0.47]
    }

    df = pd.DataFrame(default_data)
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

    X = np.array(edited_df["Konsentrasi (ppm)"]).reshape(-1, 1)
    y = np.array(edited_df["Absorbansi"])

    if len(X) >= 2:
        model = LinearRegression()
        model.fit(X, y)

        slope = model.coef_[0]
        intercept = model.intercept_
        r2 = model.score(X, y)

        st.markdown(f"""
        **Persamaan regresi:**  
        Absorbansi = {slope:.4f} × Konsentrasi + {intercept:.4f}  
        R² = {r2:.4f}
        """)

        fig, ax = plt.subplots()
        ax.scatter(X, y, color='blue', label='Data Standar')
        ax.plot(X, model.predict(X), color='green', label='Regresi Linear')
        ax.set_xlabel("Konsentrasi (ppm)")
        ax.set_ylabel("Absorbansi")
        ax.legend()
        st.pyplot(fig)

        st.session_state["slope"] = slope
        st.session_state["intercept"] = intercept
    else:
        st.warning("Masukkan minimal 2 data untuk regresi.")

# ------------------ 3. HITUNG KONSENTRASI SAMPEL -------------------
elif menu == "3. Hitung Konsentrasi Sampel":
    st.subheader("3. Hitung Konsentrasi Sampel")

    absorbansi_sampel = st.number_input("Masukkan absorbansi sampel:", min_value=0.0, step=0.01)

    # Gunakan dari session jika ada
    slope = st.session_state.get("slope", None)
    intercept = st.session_state.get("intercept", None)

    if slope is not None and intercept is not None:
        st.info(f"Menggunakan slope = {slope:.4f}, intercept = {intercept:.4f} dari kurva sebelumnya")
    else:
        slope = st.number_input("Masukkan nilai slope:", value=0.02, format="%.4f")
        intercept = st.number_input("Masukkan nilai intercept:", value=0.01, format="%.4f")

    if st.button("Hitung Konsentrasi"):
        if slope != 0:
            konsentrasi = (absorbansi_sampel - intercept) / slope
            st.success(f"Perkiraan konsentrasi: **{konsentrasi:.2f} ppm**")
        else:
            st.error("Slope tidak boleh nol.")

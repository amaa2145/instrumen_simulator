import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import io

st.set_page_config(page_title="Simulasi Instrumen Kimia", layout="centered")
st.title("🧪 Aplikasi Simulasi Instrumen Kimia")

menu = st.sidebar.radio("📋 Pilih Simulasi", [
    "1. Input Spektrum λ maks", 
    "2. Input Kurva Kalibrasi", 
    "3. Hitung Konsentrasi Sampel",
    "4. Simulasi Instrumen GC",
    "5. Simulasi Spektroskopi FTIR"
])

# ------------------ Halaman 1 -------------------
if menu == "1. Input Spektrum λ maks":

    st.subheader("1. Input Spektrum UV-Vis (λ vs Absorbansi)")

    contoh_data = "200,0.01\n250,0.18\n300,0.45\n350,0.60\n400,0.40\n450,0.25"
    input_uvvis = st.text_area("Masukkan data (λ [nm], Absorbansi)", contoh_data, height=200)

    if input_uvvis:
        try:
            import io
            df_uv = pd.read_csv(io.StringIO(input_uvvis), header=None, names=["Panjang Gelombang (nm)", "Absorbansi"])
            idx_max = df_uv["Absorbansi"].idxmax()
            lambda_max = df_uv.loc[idx_max, "Panjang Gelombang (nm)"]

            st.success(f"λ maks terdeteksi pada: **{lambda_max} nm**")

            fig, ax = plt.subplots()
            ax.plot(df_uv["Panjang Gelombang (nm)"], df_uv["Absorbansi"], color='blue')
            ax.axvline(lambda_max, color='red', linestyle='--', label=f'λ maks = {lambda_max} nm')
            ax.set_xlabel("Panjang Gelombang (nm)")
            ax.set_ylabel("Absorbansi")
            ax.set_title("Spektrum UV-Vis")
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Gagal membaca data: {e}")

# ------------------ Halaman 2 -------------------
elif menu == "2. Input Kurva Kalibrasi":
    st.subheader("2. Input Kurva Kalibrasi UV-Vis")

    contoh_kalibrasi = "0,0.01\n5,0.10\n10,0.22\n15,0.34\n20,0.45"
    input_kalibrasi = st.text_area("Masukkan data (Konsentrasi [ppm], Absorbansi)", contoh_kalibrasi, height=200)

    if input_kalibrasi:
        try:
            df_kal = pd.read_csv(io.StringIO(input_kalibrasi), header=None, names=["Konsentrasi (ppm)", "Absorbansi"])

            X = np.array(df_kal["Konsentrasi (ppm)"]).reshape(-1, 1)
            y = np.array(df_kal["Absorbansi"])

            model = LinearRegression()
            model.fit(X, y)

            slope = model.coef_[0]
            intercept = model.intercept_
            r2 = model.score(X, y)

            st.markdown(f"""
            **Persamaan Regresi:**  
            Absorbansi = {slope:.4f} × Konsentrasi + {intercept:.4f}  
            R² = {r2:.4f}
            """)

            fig, ax = plt.subplots()
            ax.scatter(X, y, color='black', label='Data Kalibrasi')
            ax.plot(X, model.predict(X), color='green', label='Garis Regresi')
            ax.set_xlabel("Konsentrasi (ppm)")
            ax.set_ylabel("Absorbansi")
            ax.set_title("Kurva Kalibrasi UV-Vis")
            ax.legend()
            st.pyplot(fig)

            # simpan hasil regresi ke session
            st.session_state["uvvis_slope"] = slope
            st.session_state["uvvis_intercept"] = intercept
        except Exception as e:
            st.error(f"Gagal membaca data: {e}")

# ------------------ Halaman 3 -------------------
elif menu == "3. Hitung Konsentrasi Sampel":
    st.subheader("3. Hitung Konsentrasi dari Absorbansi Sampel")

    absorbansi = st.number_input("Masukkan nilai absorbansi sampel:", min_value=0.0, step=0.01)

    # Ambil nilai regresi dari session
    slope = st.session_state.get("uvvis_slope", None)
    intercept = st.session_state.get("uvvis_intercept", None)

    if slope is not None and intercept is not None:
        st.info(f"Menggunakan persamaan: C = (Absorbansi - {intercept:.4f}) / {slope:.4f}")
    else:
        slope = st.number_input("Masukkan slope:", value=0.02, step=0.001)
        intercept = st.number_input("Masukkan intercept:", value=0.01, step=0.001)

    if st.button("Hitung Konsentrasi"):
        if slope != 0:
            konsentrasi = (absorbansi - intercept) / slope
            st.success(f"Konsentrasi sampel: **{konsentrasi:.2f} ppm**")
        else:
            st.error("Slope tidak boleh nol.")

    # Halaman ini dapat dikembangkan lebih lanjut

# ------------------ Halaman 4: GC -------------------
elif menu == "4. Simulasi Instrumen GC":
    st.subheader("4. Simulasi Kromatografi Gas (GC)")
    st.markdown("### 🔧 Parameter Instrumen GC")

    col1, col2 = st.columns(2)
    with col1:
        suhu_kolom = st.slider("Suhu Kolom (°C)", min_value=30, max_value=300, value=150, step=5)
        jenis_kolom = st.selectbox("Jenis Kolom", ["Kapiler", "Packed"])

    with col2:
        laju_alir = st.slider("Laju Aliran Gas Pembawa (mL/min)", min_value=1.0, max_value=5.0, value=2.0, step=0.1)
        injeksi = st.radio("Metode Injeksi", ["Manual", "Otomatis"])

    st.info(f"🧪 Suhu Kolom: {suhu_kolom}°C | Kolom: {jenis_kolom} | Alir: {laju_alir} mL/min | Injeksi: {injeksi}")

    st.markdown("Masukkan data waktu retensi dan tinggi puncak untuk setiap senyawa:")
    example_gc_data = {
        "Waktu Retensi (menit)": [1.2, 2.5, 3.7, 5.0],
        "Tinggi Puncak": [10, 25, 18, 12],
        "Lebar Puncak (menit)": [0.2, 0.3, 0.25, 0.2]
    }
    df_gc = pd.DataFrame(example_gc_data)
    edited_gc = st.data_editor(df_gc, use_container_width=True, num_rows="dynamic")

    edited_gc["Luas Puncak"] = 0.5 * edited_gc["Tinggi Puncak"] * edited_gc["Lebar Puncak (menit)"]
    total_area = edited_gc["Luas Puncak"].sum()
    edited_gc["% Area"] = (edited_gc["Luas Puncak"] / total_area) * 100

    st.markdown("### Tabel Data dan Perhitungan")
    st.dataframe(edited_gc)

    st.markdown("### Kromatogram (Simulasi)")
    fig, ax = plt.subplots()
    for index, row in edited_gc.iterrows():
        rt = row["Waktu Retensi (menit)"]
        height = row["Tinggi Puncak"]
        width = row["Lebar Puncak (menit)"]
        x_vals = [rt - width / 2, rt, rt + width / 2]
        y_vals = [0, height, 0]
        ax.plot(x_vals, y_vals, label=f"Puncak {index + 1}")

    ax.set_xlabel("Waktu Retensi (menit)")
    ax.set_ylabel("Tinggi Puncak")
    ax.set_title("Kromatogram Gas Chromatography (GC)")
    ax.legend()
    st.pyplot(fig)

# ------------------ Halaman 5: FTIR -------------------
elif menu == "5. Simulasi Spektroskopi FTIR":
    st.subheader("5. Simulasi Spektrum FTIR")
    st.markdown("Masukkan data FTIR kamu (format: bilangan gelombang [cm⁻¹] dan intensitas):")

    contoh_data = "4000,0.01\n3500,0.10\n3000,0.30\n2850,0.25\n1750,0.50\n1600,0.42\n1200,0.20\n800,0.15"
    data_input = st.text_area("Input data (wavenumber, absorbansi)", contoh_data, height=200)

    if data_input:
        try:
            df_ftir = pd.read_csv(io.StringIO(data_input), header=None, names=["Wavenumber (cm⁻¹)", "Absorbansi"])
            df_ftir.sort_values(by="Wavenumber (cm⁻¹)", ascending=False, inplace=True)

            st.markdown("### Spektrum FTIR")
            fig, ax = plt.subplots()
            ax.plot(df_ftir["Wavenumber (cm⁻¹)"], df_ftir["Absorbansi"], color='black')
            ax.set_xlabel("Bilangan Gelombang (cm⁻¹)")
            ax.set_ylabel("Absorbansi")
            ax.set_title("Spektrum FTIR")
            ax.invert_xaxis()
            st.pyplot(fig)

            st.markdown("### Identifikasi Gugus Fungsi")

            def identifikasi_gugus(wave):
                if 3700 >= wave >= 3200:
                    return "O-H / N-H (stretching)"
                elif 3100 >= wave >= 2800:
                    return "C-H (alkana, aromatik)"
                elif 1800 >= wave >= 1600:
                    return "C=O (karbonil)"
                elif 1600 >= wave >= 1400:
                    return "C=C (aromatik)"
                elif 1300 >= wave >= 1000:
                    return "C-O (alkohol, ester)"
                elif 900 >= wave >= 600:
                    return "C-H bending / fingerprint"
                else:
                    return "-"

            df_ftir["Gugus Fungsi"] = df_ftir["Wavenumber (cm⁻¹)"].apply(identifikasi_gugus)
            st.dataframe(df_ftir)

        except Exception as e:
            st.error(f"Gagal membaca data: {e}")

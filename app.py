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
menu = st.sidebar.radio("📋 Pilih Simulasi", [
    "1. Input Spektrum λ maks", 
    "2. Input Kurva Kalibrasi", 
    "3. Hitung Konsentrasi Sampel",
    "4. Simulasi Instrumen GC",
    "5. Simulasi Spektroskopi FTIR"
])

if menu == "1. Input Spektrum λ maks":
    # kode untuk UV-Vis λ maks

elif menu == "2. Input Kurva Kalibrasi":
    # kode kurva kalibrasi

elif menu == "3. Hitung Konsentrasi Sampel":
    # kode hitung sampel

elif menu == "4. Simulasi Instrumen GC":
    # kode GC

elif menu == "5. Simulasi Spektroskopi FTIR":
    # kode FTIR

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
#--------------------4. simulasi instrumen GC ----------------------
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

# Hitung luas tiap puncak (asumsi: segitiga → luas = 0.5 × tinggi × lebar)
edited_gc["Luas Puncak"] = 0.5 * edited_gc["Tinggi Puncak"] * edited_gc["Lebar Puncak (menit)"]
total_area = edited_gc["Luas Puncak"].sum()
edited_gc["% Area"] = (edited_gc["Luas Puncak"] / total_area) * 100

st.markdown("### Tabel Data dan Perhitungan")
st.dataframe(edited_gc)

# Plot kromatogram
st.markdown("### Kromatogram (Simulasi)")

fig, ax = plt.subplots()
for index, row in edited_gc.iterrows():
    rt = row["Waktu Retensi (menit)"]
    height = row["Tinggi Puncak"]
    width = row["Lebar Puncak (menit)"]

    # Buat segitiga untuk puncak GC
    x_vals = [rt - width / 2, rt, rt + width / 2]
    y_vals = [0, height, 0]
    ax.plot(x_vals, y_vals, label=f"Puncak {index + 1}")

ax.set_xlabel("Waktu Retensi (menit)")
ax.set_ylabel("Tinggi Puncak")
ax.set_title("Kromatogram Gas Chromatography (GC)")
ax.legend()
st.pyplot(fig)
#--------------------5. Simulasi FTIR ------------------
elif menu == "5. Simulasi Spektroskopi FTIR":
    st.subheader("5. Simulasi Spektrum FTIR")

    st.markdown("Masukkan data FTIR kamu (dalam format: bilangan gelombang [cm⁻¹] dan intensitas):")
    
    contoh_data = "4000,0.01\n3500,0.10\n3000,0.30\n2850,0.25\n1750,0.50\n1600,0.42\n1200,0.20\n800,0.15"
    data_input = st.text_area("Input data (wavenumber, absorbansi)", contoh_data, height=200)

    if data_input:
        try:
            import io
            df_ftir = pd.read_csv(io.StringIO(data_input), header=None, names=["Wavenumber (cm⁻¹)", "Absorbansi"])
            df_ftir.sort_values(by="Wavenumber (cm⁻¹)", ascending=False, inplace=True)  # urut dari tinggi ke rendah

            st.markdown("### Spektrum FTIR")
            fig, ax = plt.subplots()
            ax.plot(df_ftir["Wavenumber (cm⁻¹)"], df_ftir["Absorbansi"], color='black')
            ax.set_xlabel("Bilangan Gelombang (cm⁻¹)")
            ax.set_ylabel("Absorbansi")
            ax.set_title("Spektrum FTIR")
            ax.invert_xaxis()  # khas FTIR
            st.pyplot(fig)

            # Pengenalan gugus fungsi berdasarkan bilangan gelombang
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

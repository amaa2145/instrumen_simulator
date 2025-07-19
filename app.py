import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import io

st.set_page_config(page_title="Simulasi Instrumen Kimia", layout="centered")
st.title("🧪 Aplikasi Simulasi Instrumen Kimia")

# ------------------ TAMPILAN BERANDA SAJA -------------------
st.markdown("""
# 👋 Selamat Datang!

Aplikasi ini dirancang untuk mensimulasikan penggunaan berbagai **instrumen kimia** secara interaktif. Kamu bisa mencoba:
- 📊 **Spektrofotometer UV-Vis**
- 🧬 **Gas Chromatography (GC)**
- 🌈 **Spektroskopi FTIR**

st.markdown("### Pilih salah satu simulasi di bawah ini untuk memulai:")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔬 Spektrofotometer UV-Vis"):
        switch_page("spektrofotometer_uvvis")
with col2:
    if st.button("💨 Gas Chromatography (GC)"):
        switch_page("simulasi_gc")
with col3:
    if st.button("🌈 Spektroskopi FTIR"):
        switch_page("simulasi_ftir")


# ------------------ Halaman 1: UV-Vis -------------------#
st.set_page_config(page_title="Simulasi Spektrofotometer UV-Vis")
st.title("🔬 Simulasi Spektrofotometer UV-Vis")

st.markdown("""
### Panduan:
1. Tentukan panjang gelombang maksimum
2. Buat kurva kalibrasi dari data standar
3. Hitung konsentrasi sampel
""")

st.subheader("🔬 1. Simulasi Spektrum UV-Vis (λ Maksimal)")
st.markdown("Masukkan data panjang gelombang dan absorbansi:")

contoh_data = "200,0.01\n250,0.18\n300,0.45\n350,0.60\n400,0.40\n450,0.25"
input_uvvis = st.text_area("Masukkan data manual (λ [nm], Absorbansi)", contoh_data, height=150)

df_uv = None
if input_uvvis:
    try:
        lines = input_uvvis.strip().split('\n')
        data = [tuple(map(float, line.split(','))) for line in lines]
        df_uv = pd.DataFrame(data, columns=["Panjang Gelombang (nm)", "Absorbansi"])
        st.success("Data berhasil dimuat!")
        st.dataframe(df_uv)

        # Plot spektrum UV-Vis sederhana
        st.line_chart(df_uv.rename(columns={"Panjang Gelombang (nm)": "index"}).set_index("index"))

        # Deteksi lambda maks
        idx_max = df_uv["Absorbansi"].idxmax()
        lambda_max = df_uv.loc[idx_max, "Panjang Gelombang (nm)"]
        st.success(f"λ maks terdeteksi pada: **{lambda_max} nm**")

        # Opsi tampilan
        warna_garis = st.color_picker("Pilih warna garis spektrum", "#000000")
        overlay = st.checkbox("Tampilkan spektrum referensi? (simulasi)")

        # Plot lanjutan dengan Matplotlib
        fig, ax = plt.subplots()
        ax.plot(df_uv["Panjang Gelombang (nm)"], df_uv["Absorbansi"], color=warna_garis, label='Spektrum Sampel')
        ax.axvline(lambda_max, color='red', linestyle='--', label=f'λ maks = {lambda_max} nm')

        if overlay:
            ref_lambda = df_uv["Panjang Gelombang (nm)"]
            ref_abs = np.interp(ref_lambda, ref_lambda, df_uv["Absorbansi"]) * 0.8
            ax.plot(ref_lambda, ref_abs, color='gray', linestyle=':', label='Referensi')

        ax.set_xlabel("Panjang Gelombang (nm)")
        ax.set_ylabel("Absorbansi")
        ax.set_title("Spektrum UV-Vis")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Gagal membaca data teks: {e}")

        
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
    intercept = model.intercept_
    r2 = model.score(X, y)

    st.markdown(f"""
    **Persamaan regresi:**  
    f"Absorbansi = {slope:.4f} * Konsentrasi + {intercept:.4f}"
    Koefisien determinasi (R²) = {r2:.4f}
    """)

    fig, ax = plt.subplots()
    ax.scatter(X, y, color='blue', label='Data Standar')
    ax.plot(X, model.predict(X), color='green', label='Regresi Linear')
    ax.set_xlabel("Konsentrasi (ppm)")
    ax.set_ylabel("Absorbansi")
    ax.legend()
    st.pyplot(fig)

    st.subheader("3. Hitung Konsentrasi Sampel dari Absorbansi")

    st.markdown("Masukkan data berikut berdasarkan hasil kurva kalibrasi:")

    absorbansi_sampel = st.number_input(
        "Nilai absorbansi sampel:", 
        min_value=0.0, 
        step=0.01, 
        format="%.2f"
    )

    slope_input = st.number_input(
        "Nilai slope (kemiringan) dari kurva kalibrasi:", 
        value=0.025, 
        step=0.001, 
        format="%.4f"
    )

    intercept_input = st.number_input(
        "Nilai intercept (titik potong) dari kurva kalibrasi:", 
        value=0.01, 
        step=0.001, 
        format="%.4f"
    )

    if st.button("Hitung Konsentrasi"):
        try:
            konsentrasi = (absorbansi_sampel - intercept_input) / slope_input
            st.success(f"Perkiraan konsentrasi sampel: **{konsentrasi:.2f} ppm**")
        except ZeroDivisionError:
            st.error("Slope tidak boleh nol.")

# ------------------ Halaman 2: GC -------------------
elif simulasi == "GC":
    st.subheader("🧪 2. Simulasi Kromatografi Gas (GC)")
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

# ------------------ Halaman 3: FTIR -------------------
elif simulasi == "FTIR":
    st.subheader("📉 3. Simulasi Spektrum FTIR")
    st.markdown("Masukkan data FTIR kamu (format: bilangan gelombang [cm⁻¹] dan intensitas):")

    contoh_data = "4000,0.01\n3500,0.10\n3000,0.30\n2850,0.25\n1750,0.50\n1600,0.42\n1200,0.20\n800,0.15"
    data_input = st.text_area("Input data (wavenumber, absorbansi)", contoh_data, height=200)

    if data_input:
        try:
            df_ftir = pd.read_csv(io.StringIO(data_input), header=None, names=["Wavenumber (cm⁻¹)", "Absorbansi"])
            df_ftir.sort_values(by="Wavenumber (cm⁻¹)", ascending=False, inplace=True)

            st.markdown("### Spektrum FTIR")
            warna_ftir = st.color_picker("Pilih warna garis spektrum FTIR", "#000000")

            fig, ax = plt.subplots()
            ax.plot(df_ftir["Wavenumber (cm⁻¹)"], df_ftir["Absorbansi"], color=warna_ftir)
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

switch_page("1_spektrofotometer_uvvis")
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

        # ---------------- Bagian Kalibrasi ---------------- #
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

        # Tampilkan hasil regresi
        st.markdown("**Persamaan regresi:**  \nAbsorbansi = {:.4f} × Konsentrasi + {:.4f}".format(slope, intercept))
        st.markdown(f"Koefisien determinasi (R<sup>2</sup>) = {r2:.4f}", unsafe_allow_html=True)

        # Plot regresi
        fig, ax = plt.subplots()
        ax.scatter(X, y, color='blue', label='Data Standar')
        ax.plot(X, model.predict(X), color='green', label='Regresi Linear')
        ax.set_xlabel("Konsentrasi (ppm)")
        ax.set_ylabel("Absorbansi")
        ax.legend()
        st.pyplot(fig)

        # ---------------- Hitung Konsentrasi ---------------- #
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
            value=round(slope, 4), 
            step=0.001, 
            format="%.4f"
        )

        intercept_input = st.number_input(
            "Nilai intercept (titik potong) dari kurva kalibrasi:", 
            value=round(intercept, 4), 
            step=0.001, 
            format="%.4f"
        )

        if st.button("Hitung Konsentrasi"):
            try:
                konsentrasi = (absorbansi_sampel - intercept_input) / slope_input
                st.success(f"Perkiraan konsentrasi sampel: **{konsentrasi:.2f} ppm**")
            except ZeroDivisionError:
                st.error("Slope tidak boleh nol.")

    except Exception as e:
        st.error(f"Gagal membaca data teks: {e}")

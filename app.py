import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from fuzzy_model import hitung_kualitas

## GAMBAR GRAFIKK
def plot_kualitas(hasil):
    x = np.arange(0, 101, 1)

    buruk = fuzz.trimf(x, [0, 0, 40])
    cukup = fuzz.trimf(x, [30, 50, 70])
    subur = fuzz.trimf(x, [60, 100, 100])

    fig, ax = plt.subplots()

    ax.plot(x, buruk, 'r', label='Buruk')
    ax.plot(x, cukup, 'y', label='Cukup')
    ax.plot(x, subur, 'g', label='Subur')

    ax.axvline(x=hasil, color='blue', linestyle='--', label=f'Hasil: {hasil:.2f}')

    ax.set_title("Grafik Kualitas Tanah")
    ax.legend()

    return fig

# SETUP UI
st.set_page_config(page_title="Kualitas Tanah", layout="centered")

st.title("Sistem Penentuan Kualitas Tanah untuk Pertanian")
st.write("Menggunakan Fuzzy Mamdani")

# INPUT
ph = st.slider("pH Tanah", 0.0, 14.0, 7.0)
kelembaban = st.slider("Kelembaban (%)", 0, 100, 50)
nutrisi = st.slider("Nutrisi (%)", 0, 100, 50)

# PROSES
if st.button("Hitung"):
    try:
        hasil, kategori = hitung_kualitas(ph, kelembaban, nutrisi)

        st.subheader("Hasil Analisis")
        st.metric("Nilai Kualitas", round(hasil, 2))

        if "Buruk" in kategori:
            st.error(f"Kategori: {kategori}")
        elif "Cukup" in kategori:
            st.warning(f"Kategori: {kategori}")
        else:
            st.success(f"Kategori: {kategori}")

        st.info("Rekomendasi:")
        if hasil < 40:
            st.write("- Tambahkan pupuk")
            st.write("- Perbaiki pH tanah")
            st.write("- Tingkatkan kelembaban tanah")
        elif hasil < 70:
            st.write("- Optimalkan kelembaban")
            st.write("- Tambahkan nutrisi secukupnya")
        else:
            st.write("- Kondisi tanah optimal")

    except KeyError:
        st.error("Kombinasi input tidak menghasilkan output fuzzy. Coba ubah nilai input.")

    fig = plot_kualitas(hasil)
    st.pyplot(fig)
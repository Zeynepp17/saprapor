import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Excel Dosyanizi Yükleyin", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("Dosya Yüklendi!")
else:
    df = pd.read_excel("ZFMR0003 Raporu Örnek.xlsx")
    st.info("Dummy Dosyasi Gösteriliyor.")


st.set_page_config(page_title= "RAPOR", layout= "wide")
st.title(" SAP Raporu Dinamik Karşılaştırma")



aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
         "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

ay1 = st.selectbox("1. Ayı Seçin", aylar, index=0)
ay2 = st.selectbox("2. Ayı Seçin", aylar, index=1)



veri_turleri = ["Bütçe", "Fiili", "Bütçe Bakiye", "Karşılık", "ÇKG", ]
secilen_veriler = st.multiselect("Hangi veri türlerini görmek istiyorsunuz?", veri_turleri, default=["Bütçe", "Fiili"])



sabit_sutunlar = list(df.columns[:11])
secilen_sabitler = st.multiselect("Eklemek istediğiniz sabit sütunları seçin", sabit_sutunlar, default=["Masraf Yeri Adı"])

def get_sutunlar_for_ay(ay, turler):
    return [f"{ay} {tur}" for tur in turler]

sutunlar_ay1 = get_sutunlar_for_ay(ay1, secilen_veriler)
sutunlar_ay2 = get_sutunlar_for_ay(ay2, secilen_veriler)


sutunlar_ay1 = [s for s in sutunlar_ay1 if s in df.columns]
sutunlar_ay2 = [s for s in sutunlar_ay2 if s in df.columns]
secilen_sabitler = [s for s in secilen_sabitler if s in df.columns]


tum_sutunlar = secilen_sabitler + sutunlar_ay1 + sutunlar_ay2
# 
kumule_sutunlar = [col for col in df.columns if "Kümüle" in col]
secilen_kumule = st.multiselect("Kümüle verilerinden hangilerini görmek istersiniz?", kumule_sutunlar)

# 
tum_sutunlar = secilen_sabitler + sutunlar_ay1 + sutunlar_ay2 + secilen_kumule

st.subheader(f" {ay1} ve {ay2} Final Tablo")
st.dataframe(df[tum_sutunlar])

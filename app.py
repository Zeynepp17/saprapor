import streamlit as st
import pandas as pd 

st.set_page_config(page_title= "RAPOR", layout= "wide")
uploaded_file = st.file_uploader("Excel Dosyanizi Yükleyin", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("Dosya Yüklendi!")
else:
    df = pd.read_excel("ZFMR0003 Raporu Örnek.xlsx")
    st.info("Dummy Dosyasi Gösteriliyor.")

st.title("SAP Raporu Dinamik Karşılaştırma")

aylar = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
         "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

secilen_aylar= st.multiselect("Ay(lar) seçin", aylar, default=["Ocak","Şubat"]) #aylar seciliyor

kisi_listesi_dosyadan = df["Defter"].dropna().unique().tolist()
secili_kisiler = st.multiselect("Kişi Seç", kisi_listesi_dosyadan)

veri_turleri = ["Bütçe", "Fiili", "Bütçe Bakiye", "Karşılık", "ÇKG"]
secilen_veriler = st.multiselect("Hangi veri türlerini görmek istiyorsunuz?", veri_turleri, default=["Bütçe", "Fiili"])


sabit_sutunlar = list(df.columns[:11]) + ["Defter"]
secilen_sabitler = st.multiselect("Eklemek istediğiniz sabit sütunları seçin", sabit_sutunlar, default=["Masraf Yeri Adı", "Defter"])
secilen_sabitler = [s for s in secilen_sabitler if s in df.columns]

tum_sutunlar_aylar = []
for ay in secilen_aylar:
    for tur in secilen_veriler:
        sutun = f"{ay} {tur}"
        if sutun in df.columns:
            tum_sutunlar_aylar.append(sutun)


kumule_sutunlar = [col for col in df.columns if "Kümüle" in col]
secilen_kumule = st.multiselect("Kümüle verilerinden hangilerini görmek istersiniz?", kumule_sutunlar)


tum_sutunlar = secilen_sabitler + tum_sutunlar_aylar + secilen_kumule


tum_df_listesi = []
for kisi in secili_kisiler:
    df_filtered = df[df["Defter"] ==kisi].copy()
    tum_df_listesi.append(df_filtered)

if tum_df_listesi:
    df_secilikisiler = pd.concat(tum_df_listesi, ignore_index=True)
    st.subheader("Final Tablo")
    st.dataframe(df_secilikisiler[tum_sutunlar])
else:
    st.info("Lütfen en az 1 kişi seçin.")

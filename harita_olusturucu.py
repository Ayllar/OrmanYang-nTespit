import pandas as pd
import folium as fl

print("Yangın verisi okunuyor...")
try:
    df = pd.read_csv("ham_yangin_verisi.csv")
    print(f"{len(df)} adet potansiyel yangın noktası bulundu.")
except FileNotFoundError:
    print("HATA: 'ham_yangin_verisi.csv' dosyası bulunamadı.")
    print("Lütfen ilk önce veri_cekici.py scriptini çalıştırarak veriyi indirin.")
    exit()

print("Harita oluşturuluyor...")

# Harita merkezini ve başlangıç zoom seviyesini ayarla
turkiye_haritasi = fl.Map(location=[39.925533, 32.866287], zoom_start=6)

# Verideki her bir satır için döngü başlat
for index, nokta in df.iterrows():
    enlem = nokta['latitude']
    boylam = nokta['longitude']
    tarih = nokta['acq_date']
    saat = nokta['acq_time']
    guven = nokta['confidence']

    popup_metni = f"""<b>Tespit Tarihi:</b>{tarih}<br><b>Tespit Saati:</b>{saat}<br><b>Güven Seviyesi:</b>{guven}"""

    # CircleMarker oluştur ve haritaya ekle
    fl.CircleMarker(
        location=[enlem, boylam],
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.7,
        popup=fl.Popup(popup_metni, max_width=300)
    ).add_to(turkiye_haritasi)  # <--- HATA BURADAYDI, BU SATIR ÖNEMLİ

# Haritayı kaydet
turkiye_haritasi.save("alev_radari.html")
print("Harita başarıyla oluşturuldu.")
print("alev_radari.html dosyasını açarak güncel haritaya ulaşabilirsiniz")
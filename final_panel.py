import requests
import pandas as pd
import folium 
import time
import webbrowser
from io import StringIO
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image 
import os
import random

# --- AYARLAR ---
API_KEY = '09914e3deb0f840051f8a0fc89cc41cb'
SOURCE = "VIIRS_SNPP_NRT"
COUNTRY = "TR"
DAYS = "1" 
REFRESH_RATE_SECONDS = 600
MODEL_PATH = 'alev_radari_model.h5'
KARAR_ESIGI = 0.85
DATASET_DIR = 'fire_dataset' 

print("Yapay zeka modeli yükleniyor...")

# --- 1. MODEL YÜKLEME ---
try:
    # Modeli yüklemeyi dene, yoksa uyarı ver ama devam et (test için)
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
        print("Model başarıyla yüklendi.")
    else:
        print(f"UYARI: {MODEL_PATH} bulunamadı! Tahminler rastgele üretilecek.")
        model = None
except Exception as e:
    print(f"Model yüklenirken hata: {e}")
    model = None

# --- 2. RESİM VERİTABANI HAZIRLIĞI (Güvenli Mod) ---
print("Simülasyon için resim veritabanı taranıyor... ")

fire_images_path = os.path.join(DATASET_DIR, 'fire_images')
non_fire_images_path = os.path.join(DATASET_DIR, 'non_fire_images')

# Klasörler yoksa hata vermek yerine oluşturur
os.makedirs(fire_images_path, exist_ok=True)
os.makedirs(non_fire_images_path, exist_ok=True)

try:
    yangin_resimleri = [os.path.join(fire_images_path, f) for f in os.listdir(fire_images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    normal_resimleri = [os.path.join(non_fire_images_path, f) for f in os.listdir(non_fire_images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"Veritabanı: {len(yangin_resimleri)} yangın, {len(normal_resimleri)} normal resim bulundu.")
except Exception as e:
    print(f"Dosya okuma hatası: {e}")
    yangin_resimleri = []
    normal_resimleri = []

# --- 3. TAHMİN FONKSİYONU ---
def tahmin_et_yangini(image_path):
    # Eğer model yüklenemediyse sahte değer döndür
    if model is None:
        return "MODEL_YOK", 0
        
    try:
        img = image.load_img(image_path, target_size=(256, 256))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        ham_tahmin = model.predict(img_array, verbose=0)[0][0]
        ihtimal_fire = 1 - ham_tahmin 

        if ihtimal_fire > KARAR_ESIGI:
            return "YANGIN", ihtimal_fire * 100
        else:
            return "NORMAL", ihtimal_fire * 100

    except Exception as e:
        print(f"Resim işleme hatası: {e}")
        return "HATA", 0

# --- 4. NASA VERİ ÇEKME ---
def get_fire_data():
    url = f"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{API_KEY}/{SOURCE}/{COUNTRY}/{DAYS}"
    print(f"[{time.strftime('%H:%M:%S')}] NASA verileri kontrol ediliyor...")
    
    try:
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200 and len(response.text.strip().splitlines()) > 1:
            print("NASA'dan canlı veri alındı.")
            return response.text
        else:
            print("Canlı veri yok (Mevsim normali). TEST verisi kullanılıyor.")
            # Test verisi
            return """latitude,longitude,acq_date,acq_time
36.9081,30.6956,2025-11-27,1200
37.2153,28.3636,2025-11-27,1215
36.5493,31.9961,2025-11-27,1300"""

    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return None

# --- 5. HARİTA OLUŞTURMA ---
def create_map(fire_data_text):
    if not fire_data_text:
        return

    try:
        df = pd.read_csv(StringIO(fire_data_text))
    except Exception as e:
        print(f"CSV hatası: {e}")
        return

    turkiye_map = folium.Map(location=[39.925533, 32.866287], zoom_start=6)
    
    for _, nokta in df.iterrows():
        try:
            enlem = nokta['latitude']
            boylam = nokta['longitude']
            tarih = nokta['acq_date']
            
            # --- RESİM SEÇİM MANTIĞI (DÜZELTİLDİ) ---
            test_image = None
            is_fire_sim = random.choice([True, False])
            
            # Listeler boşsa hata vermemesi için kontroller:
            if is_fire_sim and yangin_resimleri:
                test_image = random.choice(yangin_resimleri)
            elif normal_resimleri:
                test_image = random.choice(normal_resimleri)
            
            # Resim varsa tahmin yap, yoksa varsayılan değer ata
            if test_image and os.path.exists(test_image):
                sonuc, ihtimal = tahmin_et_yangini(test_image)
            else:
                sonuc = "RESİM_YOK"
                ihtimal = 0

            # Renk ve İkon Ayarları
            if sonuc == "YANGIN":
                renk = 'red'
                ikon = 'fire'
                mesaj = "YANGIN TESPİT EDİLDİ"
            elif sonuc == "NORMAL":
                renk = 'green'
                ikon = 'tree'
                mesaj = "GÜVENLİ BÖLGE"
            else:
                renk = 'gray'
                ikon = 'question'
                mesaj = "GÖRÜNTÜ ALINAMADI"

            popup_text = f"""
            <b>Durum:</b> {mesaj}<br>
            <b>Olasılık:</b> %{ihtimal:.2f}<br>
            <b>Kaynak:</b> {os.path.basename(test_image) if test_image else 'Veri Yok'}
            """

            folium.Marker(
                location=[enlem, boylam],
                icon=folium.Icon(color=renk, icon=ikon, prefix='fa'),
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(turkiye_map)

        except Exception as e:
            print(f"Nokta işleme hatası: {e}")
            continue

    output_file = "final_alev_radari.html"
    turkiye_map.save(output_file)
    print(f"HARİTA GÜNCELLENDİ: {output_file}")

# --- ANA PROGRAM ---
if __name__ == "__main__":
    print("Sistem Başlatılıyor...")
    while True:
        data = get_fire_data()
        if data:
            create_map(data)
        print(f"{REFRESH_RATE_SECONDS} saniye bekleniyor...")
        time.sleep(REFRESH_RATE_SECONDS)
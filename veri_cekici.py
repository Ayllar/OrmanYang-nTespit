{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "dd8d0bf1-d8ce-4564-89b9-22a755513130",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "NASA FIRMS sunucusuna bağlanıyor...\n",
      "İstek gönderilen URL: https://firms.modaps.eosdis.nasa.gov/api/country/csv/09914e3deb0f840051f8a0fc89cc41cb/VIIRS_SNPP_NRT/TUR/1\n",
      "\n",
      "Bağlantı Başarılı! Veri alınıyor...\n",
      "\n",
      "Veri 'ham_yangin_verisi.csv' dosyasına başarıyla kaydedildi!\n"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "\n",
    "API_KEY =\"09914e3deb0f840051f8a0fc89cc41cb\"\n",
    "\n",
    "SOURCE = \"VIIRS_SNPP_NRT\"\n",
    "COUNTRY = \"TUR\"\n",
    "DAYS = \"1\"\n",
    "\n",
    "# URL oluşturuluyor\n",
    "url = f\"https://firms.modaps.eosdis.nasa.gov/api/country/csv/{API_KEY}/{SOURCE}/{COUNTRY}/{DAYS}\"\n",
    "\n",
    "print(\"NASA FIRMS sunucusuna bağlanıyor...\")\n",
    "print(f\"İstek gönderilen URL: {url}\")\n",
    "\n",
    "try:\n",
    "    response = requests.get(url)\n",
    "    \n",
    "    if response.status_code == 200:\n",
    "        print(\"\\nBağlantı Başarılı! Veri alınıyor...\")\n",
    "        fire_data_text = response.text\n",
    "        \n",
    "        # Veriyi kaydet\n",
    "        with open(\"ham_yangin_verisi.csv\", \"w\", encoding=\"utf-8\") as file:\n",
    "            file.write(fire_data_text)\n",
    "            \n",
    "        print(\"\\nVeri 'ham_yangin_verisi.csv' dosyasına başarıyla kaydedildi!\")\n",
    "    else:\n",
    "        print(f\"\\nHata! Durum kodu: {response.status_code}\")\n",
    "        print(\"Sunucunun cevabı :\", response.text)\n",
    "\n",
    "except Exception as e:\n",
    "    print(f\"Program çalışırken bir hata oluştu: {e}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "a573c8c4-f721-4c0e-b729-4399f2ea854a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}

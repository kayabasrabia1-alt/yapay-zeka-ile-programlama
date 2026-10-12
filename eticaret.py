import json
import os

# Kütüphane yüklü mü kontrol edelim, değilse kullanıcıyı yönlendirelim
try:
    import google.generativeai as genai
except ImportError:
    print("[HATA] 'google-generativeai' kütüphanesi yüklü değil!")
    print("Lütfen terminale: pip install google-generativeai yazarak yükleyin.")
    exit()

# Gemini API Yapılandırması
if "GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
else:
    print("[UYARI] GEMINI_API_KEY çevre değişkeni bulunamadı! API çağrıları başarısız olabilir.")

DOSYA_ADI = "urunler.json"

def veri_yukle():
    """urunler.json dosyasından mevcut ürünleri yükler, dosya yoksa boş liste döndürür."""
    if not os.path.exists(DOSYA_ADI):
        return []
    try:
        with open(DOSYA_ADI, "r", encoding="utf-8") as dosya:
            return json.load(dosya)
    except (json.JSONDecodeError, Exception):
        print("[UYARI] urunler.json dosyası bozuk veya boş. Yeni liste ile başlanıyor.")
        return []

def veri_kaydet(urunler):
    """Ürün listesini urunler.json dosyasına kaydeder."""
    try:
        with open(DOSYA_ADI, "w", encoding="utf-8") as dosya:
            json.dump(urunler, dosya, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"[HATA] Dosya kaydedilirken bir hata oluştu: {e}")

def e_ticaret_api_simulasyonu(urun_aciklamasi):
    """Gemini API kullanarak ürün açıklamasını analiz eder ve sözlük (dict) döndürür."""
    prompt = f"""
    Aşağıdaki ürün açıklamasını analiz et ve JSON formatında şu anahtarlarla yanıt ver:
    - urun_adi (string)
    - kategori (string)
    - seo_etiketleri (string, virgülle ayrılmış 3 etiket)
    - satis_aciklamasi (string, tam olarak iki cümlelik satış açıklaması)

    Ürün Açıklaması: {urun_aciklamasi}
    """
    
    try:
        # Doğru Gemini modelini çağırıyoruz
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        veri = json.loads(response.text)
        return veri
    except Exception as e:
        print(f"[HATA] API çağrısı sırasında bir sorun oluştu: {e}")
        return None

def yeni_urun_ekle(urunler):
    """1. Seçenek: Yeni ürün ekler, API ile analiz eder ve kaydeder."""
    print("\n--- Yeni Ürün Ekle ---")
    urun_aciklamasi = input("Ürün açıklaması: ").strip()
    if not urun_aciklamasi:
        print("[HATA] Ürün açıklaması boş olamaz.")
        return

    try:
        fiyat = float(input("Ürün fiyatı: "))
        if fiyat < 0:
            print("[HATA] Fiyat negatif olamaz.")
            return
    except ValueError:
        print("[HATA] Geçersiz fiyat girdisi. Sayı girmelisiniz.")
        return

    try:
        stok = int(input("Stok miktarı: "))
        if stok < 0:
            print("[HATA] Stok miktarı negatif olamaz.")
            return
    except ValueError:
        print("[HATA] Geçersiz stok girdisi. Tam sayı girmelisiniz.")
        return

    print("[API] Ürün bilgileri oluşturuluyor...")
    api_sonuc = e_ticaret_api_simulasyonu(urun_aciklamasi)
    
    if not api_sonuc:
        print("[HATA] Ürün bilgileri üretilemedi.")
        return

    yeni_id = len(urunler) + 1
    urun_kodu = f"URN-{yeni_id:04d}"

    yeni_urun = {
        "urun_kodu": urun_kodu,
        "urun_adi": api_sonuc.get("urun_adi", "Bilinmiyor"),
        "kategori": api_sonuc.get("kategori", "Bilinmiyor"),
        "seo_etiketleri": api_sonuc.get("seo_etiketleri", ""),
        "satis_aciklamasi": api_sonuc.get("satis_aciklamasi", ""),
        "fiyat": fiyat,
        "stok": stok
    }

    urunler.append(yeni_urun)
    veri_kaydet(urunler)

    print("[BAŞARILI] Ürün kaydedildi.")
    print(f"Ürün Kodu       : {yeni_urun['urun_kodu']}")
    print(f"Ürün Adı        : {yeni_urun['urun_adi']}")
    print(f"Kategori        : {yeni_urun['kategori']}")
    print(f"Fiyat           : {yeni_urun['fiyat']} TL")
    print(f"Stok            : {yeni_urun['stok']}")
    print(f"SEO             : {yeni_urun['seo_etiketleri']}")

    if yeni_urun['stok'] == 0:
        print("[UYARI] STOKTA YOK")
    elif 1 <= yeni_urun['stok'] <= 4:
        print(f"[UYARI] KRİTİK STOK! Yalnızca {yeni_urun['stok']} adet kaldı.")

def urunleri_listele(urunler):
    """2. Seçenek: Kayıtlı tüm ürünleri listeler."""
    print("\n--- Ürünleri Listele ---")
    if not urunler:
        print("[UYARI] Liste boş. Henüz kayıtlı ürün bulunmamaktadır.")
        return

    for u in urunler:
        print(f"Kod: {u['urun_kodu']} | Ad: {u['urun_adi']} | Kategori: {u['kategori']} | Fiyat: {u['fiyat']} TL | Stok: {u['stok']}")

def urun_ara(urunler):
    """3. Seçenek: Ürün adı veya koduyla büyük/küçük harf duyarsız arama yapar."""
    print("\n--- Ürün Ara ---")
    if not urunler:
        print("[UYARI] Aranacak kayıt bulunamadı (Liste boş).")
        return

    aranan = input("Aranacak ürün (ad veya kod): ").strip().lower()
    if not aranan:
        print("[HATA] Arama terimi boş olamaz.")
        return

    bulunanlar = [
        u for u in urunler 
        if aranan in u['urun_kodu'].lower() or aranan in u['urun_adi'].lower()
    ]

    if bulunanlar:
        print(f"[SONUÇ] {len(bulunanlar)} ürün bulundu:")
        for u in bulunanlar:
            print(f"-> Kod: {u['urun_kodu']}, Adı: {u['urun_adi']}, Fiyat: {u['fiyat']} TL, Stok: {u['stok']}")
    else:
        print("[SONUÇ] Eşleşen ürün bulunamadı.")

def stok_guncelle(urunler):
    """4. Seçenek: Ürün koduna göre stok miktarını günceller."""
    print("\n--- Stok Güncelle ---")
    if not urunler:
        print("[UYARI] Güncellenecek ürün yok (Liste boş).")
        return

    kod = input("Ürün kodu (örn: URN-0001): ").strip().upper()
    
    hedef_urun = next((u for u in urunler if u['urun_kodu'] == kod), None)

    if not hedef_urun:
        print("[HATA] Bu koda sahip ürün bulunamadı.")
        return

    try:
        yeni_stok = int(input("Yeni stok miktarı: "))
        if yeni_stok < 0:
            print("[HATA] Stok miktarı negatif olamaz.")
            return
    except ValueError:
        print("[HATA] Geçersiz stok girdisi. Tam sayı girmelisiniz.")
        return

    eski_stok = hedef_urun['stok']
    hedef_urun['stok'] = yeni_stok
    veri_kaydet(urunler)

    print(f"[BAŞARILI] Stok {eski_stok} -> {yeni_stok} olarak güncellendi.")

    if yeni_stok == 0:
        print("[UYARI] STOKTA YOK")
    elif 1 <= yeni_stok <= 4:
        print("[UYARI] KRİTİK STOK!")

def main():
    """Ana program döngüsü ve menü yönetimi."""
    urunler = veri_yukle()

    while type(urunler) is list:
        print("\n== E-TICARET YÖNETİM PANELI ==")
        print("1 Yeni Ürün Ekle")
        print("2 Ürünleri Listele")
        print("3 Ürün Ara")
        print("4 Stok Güncelle")
        print("5 - Çıkış")
        
        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            yeni_urun_ekle(urunler)
        elif secim == "2":
            urunleri_listele(urunler)
        elif secim == "3":
            urun_ara(urunler)
        elif secim == "4":
            stok_guncelle(urunler)
        elif secim == "5":
            print("Programdan çıkılıyor. İyi günler!")
            break
        else:
            print("[HATA] Geçersiz seçim yaptınız. Lütfen 1-5 arasında bir sayı girin.")

if __name__ == "__main__":
    main()
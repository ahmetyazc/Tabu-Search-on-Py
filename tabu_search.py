import random
import numpy as np

def txt_to_matrix(dosya_yolu):
  try:
      with open(dosya_yolu, 'r') as file:
          satirlar = file.readlines()
          matrix = [list(map(int, satir.split())) for satir in satirlar]
          
          return matrix
  except FileNotFoundError:
      print(f"Dosya '{dosya_yolu}' bulunamadı.")
      return None

sehir_matrix = txt_to_matrix("distance.txt")

sehir_sayisi = len(sehir_matrix)

def yol_mesafesi(sehirler, matris):
    # Verilen bir yolun toplam mesafesini hesaplar
    mesafe = 0
    for i in range(len(sehirler) - 1):
        sehir1 = sehirler[i]
        sehir2 = sehirler[i + 1]
        mesafe += matris[sehir1][sehir2]
    return mesafe

sehirler = list(range(sehir_sayisi))

def rastgele_yol_alma():
    random.shuffle(sehirler)  # Rastgele yol oluşturmak için şehirleri karıştır
    return sehirler

aranan_sayi = int(input("Dizide aramak istediğiniz sayıyı girin: "))

def sayi_bul_ve_degistir(dizi, aranan_sayi):
    if aranan_sayi not in dizi:
        print("Aranan sayı dizide bulunamadı.")
        return

    ilk_eleman_index = dizi.index(aranan_sayi)
    dizi[0], dizi[ilk_eleman_index] = dizi[ilk_eleman_index], dizi[0]
    print("Dizi, ilk elemanla aranan sayıyı yer değiştirerek şu şekilde güncellendi:", dizi)

sayi_bul_ve_degistir(sehirler, aranan_sayi)

en_iyi_yol = sehirler.copy()
en_iyi_mesafe = yol_mesafesi(en_iyi_yol, sehir_matrix)
tabu_listesi = []

def tabu_search(iterasyon_sayisi):
    global sehirler, en_iyi_yol, en_iyi_mesafe

    for iterasyon in range(iterasyon_sayisi):
        en_iyi_komsu = None
        en_iyi_komsu_mesafe = float('inf')

        for i in range(len(sehirler) - 1):
            for j in range(i + 1, len(sehirler)):
                komsu_yol = sehirler.copy()
                komsu_yol[i], komsu_yol[j] = komsu_yol[j], komsu_yol[i]
                komsu_mesafe = yol_mesafesi(komsu_yol, sehir_matrix)

                if komsu_mesafe < en_iyi_komsu_mesafe and (i, j) not in tabu_listesi:
                    en_iyi_komsu = komsu_yol
                    en_iyi_komsu_mesafe = komsu_mesafe

        sehirler = en_iyi_komsu
        if en_iyi_komsu_mesafe < en_iyi_mesafe:
            en_iyi_yol = sehirler
            en_iyi_mesafe = en_iyi_komsu_mesafe

        for tabu_suresi in range(len(tabu_listesi)):
            if tabu_suresi == 5:
                tabu_listesi.pop(0)

    return en_iyi_yol, en_iyi_mesafe

gidilen_mesafe = yol_mesafesi(sehirler, sehir_matrix)

print("Oluşturulan Rastgele Yol:", sehirler)
print("Gidilen Mesafe:", gidilen_mesafe)

en_iyi_yol, en_iyi_mesafe = tabu_search(1000)

print("En İyi Yol:", en_iyi_yol)
print("En İyi Mesafe:", en_iyi_mesafe)
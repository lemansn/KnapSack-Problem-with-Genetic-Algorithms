
# Kütüphaneler
import numpy as np
import random
import matplotlib.pyplot as plt

plt.style.use('ggplot')


# Ürünlerin bilgilerini tutacak olan sınıf
class Urun:

    def __init__(self, id, value, weight):
        self.id = id  # ürün ismini tutar
        self.weight = weight  # ürünün ağırlığını tutar
        self.value = value  # ürünün değerini tutar


# Sırt çantası kombinasyonların tutacak olan nesne
class Knapsack:

    def __init__(self, urun_sayisi):
        # secilen ürünler listesini boolean değerler kullanarak oluştururuz
        self.secilen_urunler = np.random.randint(2, size=urun_sayisi)

    # seçilen sırt çantası için fitness değeri hesaplar ve geri döndürür
    def fitness_hesaplama(self, urun_listesi, max_agirlik):

        fitness = 0
        toplam_agirlik = 0
        for sayac in range(len(urun_listesi)):
            fitness += urun_listesi[sayac].value * self.secilen_urunler[sayac]
            toplam_agirlik += urun_listesi[sayac].weight * self.secilen_urunler[sayac]
            if toplam_agirlik > max_agirlik:
                fitness = 0
                break

        return fitness


# Ürün nesnelerini dosyadan okuyarak oluşturan ve liste içine atan fonk
# Aynı zamanda ürün oluşturulduktan sonra bilgilerini ekrana yazdırır
# bütün okuma bittikten sonra bir tablo oluşmuş olur
def urun_olustur():

    urunler = []
    dosya = open("dataSet", "r", encoding="utf-8")
    print("Dosya Içindekiler:\n")
    for satir in dosya:
        kelimeler = satir.split()
        nesne = Urun(kelimeler[0], int(kelimeler[2]), int(kelimeler[1]))
        urunler.append(nesne)
        print(format(nesne.id, "9"), format(nesne.weight, "12"), format(nesne.value, "9"))

    return urunler


# Sırt çantalarının fitness değerlerine göre populasyonu sort eder
def sort_knapsacks(populasyon, urun_listesi, max_agirlik):

    # en düşük fitness değerinden en büyük olana doğru
    return sorted(populasyon, key=lambda canta: canta.fitness_hesaplama(urun_listesi, max_agirlik))

# Genetik algoritmada kullanılan selection işlemi
def selection(populasyon, urun_listesi, max_agirlik):

    populasyon = sort_knapsacks(populasyon, urun_listesi, max_agirlik)
    return populasyon[int(90 * len(populasyon) / 100):]  # ilk %10 direk gelecek nesile aktarılır

# Genetik algoritmada kullanılan crossover işlemi
# Oluşturulan yeni nesil geri döndürülür
def crossover(parent1, parent2):

    child = parent1.secilen_urunler.copy()
    for i in range(len(child)):
        prob = random.random()

        if prob < 0.45:  # birinci
            child[i] = parent1.secilen_urunler[i]

        elif prob < 0.9:  # ikinci
            child[i] = parent2.secilen_urunler[i]

        else:  # mutasyon
            child[i] = np.random.randint(2)

    # Yeni nesil oluşturuldu
    offspring = Knapsack(len(child))
    offspring.secilen_urunler = child

    return offspring


# Bulunan çözümleri karşılaştırmak için kullanılan asıl algoritma buradadır.
# Recursion fonk kullanılır
def knapsack(max_agirlik, weights, values, urun_sayisi):

    # Daha fazla bakılacak çözüm yoksa ve bakılacak başka ürün yoksa koşula girer
    if urun_sayisi == 0 or max_agirlik == 0:
        return 0

    # Ağılığı kapasiteden daha büyük olan ağırlıklı ürünü çıkartıp fonk bir kere daha çağırır (recursion)
    if weights[urun_sayisi - 1] > max_agirlik:
        return knapsack(max_agirlik, weights, values, urun_sayisi - 1)

    else:
        al = values[urun_sayisi - 1] + knapsack(max_agirlik - weights[urun_sayisi - 1], weights, values,
                                                (urun_sayisi - 1))
        alma = knapsack(max_agirlik, weights, values, urun_sayisi - 1)
        return max(al, alma)  # Durumlara bakılır ve değeri en büyük olan tercih edilir


# En optimum sonucun bulunduğu popülasyon içinde ürünlerin sırt çantalarına kaç defa seçildiğini hesaplar
def hangi_urun_kac_defa_secildi(populasyon, liste):

    for i in range(20):
        for j in range(len(liste)):
            if 1 == populasyon[i].secilen_urunler[j]:
                liste[j] += 1
    return liste


def main():

    max_agirlik = 150  # Çantada tutulabilecek max ağırlık
    urun_listesi = urun_olustur()  # Ürünlerden nesneler oluşturulur
    populasyon_boyutu = 20  # Populasyonun max boyutu
    jenerasyon = 1
    max_jenerasyon = 50  # Oluşturulabilecek maximum jenerasyon sayısı
    populasyon = []  # Sırt çantalarını bulunduğu popülasyon
    mean_fitness_history = []  # grafik oluşturulurken kullanılacak liste
    max_fitness_history = []  # grafik oluşturulurken kullanılacak liste
    liste = [0]*len(urun_listesi)  # Hangi ürünün kaç defa sırt çantasına eklendiği bilgisini tutacak olan liste

    degerler = [canta.value for canta in urun_listesi]
    agirliklar = [canta.weight for canta in urun_listesi]
    en_iyi_cozum = knapsack(max_agirlik, agirliklar, degerler, len(urun_listesi))

    # Birinci nesil oluşturulur
    for _ in range(populasyon_boyutu):
        populasyon.append(Knapsack(len(urun_listesi)))

    # fitness değerlerlerini kaydederiz
    mean_fitness_history.append(sum(canta.fitness_hesaplama(urun_listesi, max_agirlik)\
                                    for canta in populasyon) / populasyon_boyutu)
    cozum = sort_knapsacks(populasyon, urun_listesi, max_agirlik)[-1] \
        .fitness_hesaplama(urun_listesi, max_agirlik)
    max_fitness_history.append(cozum)

    # En iyi çözüm ve elimizdeki çözüm birbirleriyle aynı değilse ve maximum jenerasyon sayısını
    # aşmadıysak while döngüsü içinde yeniden jenerasyonlar oluşturulmaya devam edilir
    while jenerasyon < max_jenerasyon or en_iyi_cozum != cozum:

        # Selection/Elitism
        yeni_jenerasyon = selection(populasyon, urun_listesi, max_agirlik)

        # Crossover & Mutation
        # Direk aktarılan %10 dışında oluşturulacak %90lık kısım burada alınır
        # En iyi %50 içinden seçimler yapılır
        kesim = int((90 * populasyon_boyutu) / 100)
        en_iyiler= populasyon[int(populasyon_boyutu * 0.5):]

        for _ in range(kesim):
            parent1 = random.choice(en_iyiler)

            parent2 = random.choice(en_iyiler)
            yeni_jenerasyon.append(crossover(parent1, parent2))

        populasyon = yeni_jenerasyon  # yeni popülasyon

        # fitness değerlerlerini kaydederiz
        mean_fitness_history.append(sum(canta.fitness_hesaplama(urun_listesi, max_agirlik) \
                                        for canta in populasyon) / populasyon_boyutu)
        cozum = sort_knapsacks(populasyon, urun_listesi, max_agirlik)[-1] \
            .fitness_hesaplama(urun_listesi, max_agirlik)
        max_fitness_history.append(cozum)
        jenerasyon += 1

    hangi_urun_kac_defa_secildi(populasyon, liste)

    # Popülasyon içinden en iyi fitness değerine sahip olan çantayı çanta içindeki ürünlerin bilgilerini
    # yazdırmak için seçiyoruz
    optimal = sorted(populasyon, key=lambda canta:
    canta.fitness_hesaplama(urun_listesi, max_agirlik))[-1]

    print('\nGA {} jenerasyonda en optimal çözüm olarak bunu bulmuştur:'.format(jenerasyon))
    print('\nÜrün Adı\t\t\tAğırlık  \tDeğer')
    print("--------------------------------------------------------")

    # optimal çanta içindeki verileri knapsack_0_1 listesi içine atıyoruz
    knapsack_0_1 = [0]*len(urun_listesi)
    for i in range(len(urun_listesi)):
        if optimal.secilen_urunler[i]:
            knapsack_0_1[i] =1
            print(format(urun_listesi[i].id, "9"), format(urun_listesi[i].weight, "16"),
                  format(urun_listesi[i].value, "9"))


    # Fitness değerini ve optimal çözümü ekrana yazdırıyoruz.
    print('\nFitness: {}'.format(optimal.fitness_hesaplama(urun_listesi, max_agirlik)))
    print('The Knapsack 0/1 Optimal Çözüm {} dir'.format(en_iyi_cozum))

    # Sırt çantasına seçilen ürünleri ekrana yazdırıyoruz
    print("\nSeçilenler:")
    for i in range(len(urun_listesi)):
        print(knapsack_0_1[i], " ", end='')

    liste2 = [" "]*len(urun_listesi)
    i = -1

    for urun in urun_listesi:
        i=i+1

        liste2[i] =urun.id


    # Ürünlerin kaç defa sırt çantalarına eklendiği bilgisini ekrana çıkacak
    x_pos = [i for i, _ in enumerate(liste2)]
    plt.bar(x_pos, liste, color='green')
    plt.xlabel('Ürün Adı')
    plt.ylabel('Ürün Kaç Defa Seçildi')
    plt.xticks(x_pos, liste2)
    plt.show()
    plt.ioff()


    plt.pie(liste, labels = liste2)
    plt.show()

    # Optimal çözüm bulunurken her jenerasyonda gözlemlenen fitness değerleriyle oluşturulacak olan grafik
    plt.plot(list(range(jenerasyon)), mean_fitness_history, label='Mean Fitness')
    plt.plot(list(range(jenerasyon)), max_fitness_history, label='Max Fitness')
    plt.legend()
    plt.title('Fitness vs. Jenerasyonlar')
    plt.xlabel('Jenerasyonlar')
    plt.ylabel('Fitness')
    plt.show()


main()

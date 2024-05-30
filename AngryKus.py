import pygame
import math

pygame.init()
ekran_genisligi = 800
ekran_yuksekligi = 600
ekran = pygame.display.set_mode((ekran_genisligi, ekran_yuksekligi))
pygame.display.set_caption("Angry Kuş")

BEYAZ = (255, 255, 255)
KIRMIZI = (255, 0, 0)
SIYAH = (0, 0, 0)
FPS = 60
saat = pygame.time.Clock()

class Kus:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.hiz_x = 0
        self.hiz_y = 0
        self.ucluyor = False
        self.yercekimi = 0.5  # Yerçekimi ivmesi
        self.puan = 0
        self.oyun_bitti = False

    def ciz(self, ekran):
        pygame.draw.circle(ekran, KIRMIZI, (int(self.x), int(self.y)), self.radius)

    def guncelle(self):
        if self.ucluyor:
            # Fırlatma açısına göre hareket et
            self.x += self.hiz_x
            self.y += self.hiz_y
            # Yerçekimi etkisi
            self.hiz_y += self.yercekimi  # Dikey hızın artması (yerçekimi etkisi)
            # Kenar kontrolü
            if self.x > ekran_genisligi - self.radius or self.x < self.radius:
                self.ucluyor = False
                self.hiz_x = 0
                self.hiz_y = 0
                self.puan = 0
                self.oyun_bitti = True  # Duvara çarptığında oyunu bitir
            # Zeminle çarpışma kontrolü
            if self.y > ekran_yuksekligi - self.radius:
                self.ucluyor = False
                self.y = ekran_yuksekligi - self.radius
                self.hiz_y = 0
                if self.x > ekran_genisligi - self.radius or self.x < self.radius:
                    self.puan = 0  # Eğer kenara çarpıp düşüyorsa puanı sıfırla
                    self.oyun_bitti = True  # Kenara çarpıp düşerse oyunu bitir
                else:
                    self.puan = int(self.x - 100)  # Fırlatma başlangıç noktasına göre puan hesapla
                    self.oyun_bitti = True  # Yere düşerse oyunu bitir

def ciz_ok(ekran, baslangic, bitis):
    pygame.draw.line(ekran, SIYAH, baslangic, bitis, 5)
    # Ok ucunu çiz
    delta_x = bitis[0] - baslangic[0]
    delta_y = bitis[1] - baslangic[1]
    angle = math.atan2(delta_y, delta_x)
    uc_uzunluk = 10
    uc_acisi = math.pi / 6
    uclari = [
        (bitis[0] - uc_uzunluk * math.cos(angle - uc_acisi), bitis[1] - uc_uzunluk * math.sin(angle - uc_acisi)),
        (bitis[0] - uc_uzunluk * math.cos(angle + uc_acisi), bitis[1] - uc_uzunluk * math.sin(angle + uc_acisi))
    ]
    pygame.draw.line(ekran, SIYAH, bitis, uclari[0], 5)
    pygame.draw.line(ekran, SIYAH, bitis, uclari[1], 5)

kus = Kus(100, ekran_yuksekligi - 50)
ok_baslangic = (kus.x, kus.y)
ok_bitis = (kus.x, kus.y)
fare_tiklandi = False
calisiyor = True

while calisiyor:
    for etkinlik in pygame.event.get():
        if etkinlik.type == pygame.QUIT:
            calisiyor = False
        elif etkinlik.type == pygame.MOUSEBUTTONDOWN:
            if not kus.ucluyor and not kus.oyun_bitti:
                fare_tiklandi = True
                ok_baslangic = (kus.x, kus.y)
                ok_bitis = pygame.mouse.get_pos()
        elif etkinlik.type == pygame.MOUSEBUTTONUP:
            if fare_tiklandi:
                fare_tiklandi = False
                # Fırlatma açısını ve hızını hesapla
                delta_x = ok_bitis[0] - ok_baslangic[0]
                delta_y = ok_bitis[1] - ok_baslangic[1]
                hiz = math.sqrt(delta_x ** 2 + delta_y ** 2) / 10  # Hızı ayarlayın
                kus.hiz_x = hiz * math.cos(math.atan2(delta_y, delta_x))
                kus.hiz_y = hiz * math.sin(math.atan2(delta_y, delta_x))
                kus.ucluyor = True
        elif etkinlik.type == pygame.MOUSEMOTION:
            if fare_tiklandi:
                ok_bitis = pygame.mouse.get_pos()

    ekran.fill(BEYAZ)
    if fare_tiklandi:
        ciz_ok(ekran, ok_baslangic, ok_bitis)
    kus.guncelle()
    kus.ciz(ekran)

    # Puanı ekranda göster
    if kus.oyun_bitti:
        pygame.draw.rect(ekran, BEYAZ, (250, 200, 300, 200))
        pygame.draw.rect(ekran, SIYAH, (250, 200, 300, 200), 2)
        if kus.puan > 0:
            mesaj = f"Oyunu kazandınız! Puan: {kus.puan}"
        else:
            mesaj = "Oyunu kaybettiniz! Puan: 0"
        mesaj_yazi = pygame.font.SysFont(None, 36).render(mesaj, True, SIYAH)
        ekran.blit(mesaj_yazi, (300, 280))
    else:
        puan_yazi = pygame.font.SysFont(None, 36).render(f"Puan: {kus.puan}", True, SIYAH)
        ekran.blit(puan_yazi, (10, 10))

    pygame.display.flip()
    saat.tick(FPS)

pygame.quit()

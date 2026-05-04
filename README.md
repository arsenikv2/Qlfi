<h1 align="center">
  <br>
  🐍 Q LFI V1 - Ultimate Auto-Exploit Scanner
  <br>
</h1>

<h4 align="center">Developed by <a href="https://github.com/arsenikv2" target="_blank">Arsenik</a></h4>

<p align="center">
  <a href="#-özellikler">✨ Özellikler</a> •
  <a href="#-kurulum">📦 Kurulum</a> •
  <a href="#-kullanım">🚀 Kullanım</a> •
  <a href="#-payload-modülleri">💣 Payload Modülleri</a> •
  <a href="#️-uyarı">⚠️ Uyarı</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-V1-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Language-Python3-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Ultimate-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Developer-Arsenik-orange?style=for-the-badge">
</p>

---

## 🌌 Giriş

**Q LFI V1**, **Local File Inclusion (LFI)** zafiyetlerini tespit etmek ve sömürmek için geliştirilmiş, Python ile yazılmış **nihai otomatik saldırı çerçevesidir**. 

LFI-Striker'dan ilham alınarak yeniden tasarlanan bu araç, statik taramaların ötesine geçer; **akıllı parametre keşfi**, **150+ elite payload**, **otomatik exploit zincirleri** ve **gelişmiş bypass teknikleri** ile hedef sistemdeki en derin zafiyetleri bile ortaya çıkarır. Tek bir komutla hedefi analiz eder, zafiyeti doğrular ve kritik dosyaları otomatik olarak elde eder.

> 🔥 *"Gölgede kalan her dosya yolu, Q LFI ile aydınlanır."*

---

## ✨ Özellikler

| 🧠 Akıllı Tespit | 🚀 Yüksek Performans | 🛡️ Gelişmiş Modüller |
|:---:|:---:|:---:|
| **Otomatik Parametre Keşfi** | **Multi-Thread Tarama** | **PHP Filter Chain RCE** |
| **Diferansiyel Analiz** | **Eşzamanlı İstekler** | **Log Poisoning Exploit** |
| **Base64 Decode Kontrolü** | **Gecikme & Timeout Ayarı** | **Proc FD Enjection** |
| **Response Pattern Match** | **Localhost Optimizasyonu** | **Wrapper Bypass** |

### 💎 Öne Çıkanlar
- 🤖 **Tam Otomatik Tarama:** URL'yi verin; parametre bulma, test etme ve exploit etme işlemlerini Q LFI halletsin.
- 🔥 **150+ Elite Payload:** Temel traversal'dan karmaşık filter chain'lere kadar kapsamlı payload kütüphanesi.
- 💥 **Auto-Exploit:** Zafiyet tespit edildiğinde otomatik olarak `/etc/passwd`, `config.php` okuma ve RCE denemeleri.
- 🔍 **Smart Fuzzing:** URL'de parametre yoksa 80+ yaygın parametreyi otomatik olarak dener.
- 🎭 **60+ User-Agent:** Bot, tarayıcı ve mobil ajanlarla WAF/IDS atlatma.
- 📊 **Detaylı Raporlama:** Sonuçları JSON ve TXT formatında kapsamlı raporlar.
- 🏠 **Localhost Desteği:** `localhost`, `127.0.0.1` ve özel portlar için tam uyumluluk.
- 📦 **Tek Dosya:** Harici bağımlılık dosyası gerektirmez, kurulumu son derece basittir.

---

## 📦 Kurulum

Q LFI V1, tek dosya yapısı sayesinde hızlıca kurulup çalıştırılabilir.

### 🐍 Gereksinimler
- Python 3.x
- `requests` ve `colorama` kütüphaneleri

### 🛠️ Adımlar

```bash
# 1. Repoyu klonlayın veya scripti indirin
git clone https://github.com/arsenik/Qlfi.git
cd Qlfi
# 2. Gerekli kütüphaneleri yükleyin
pip3 install requests colorama
# Eğer pip komutu bulunamazsa:
python3 -m pip install requests colorama

# 3. Scripti çalıştırılabilir yapın
chmod +x q_lfi.py

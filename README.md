# Proyek Aplikasi Tracker Shuttle Intrakampus ITB Jatinangor

Aplikasi pelacak posisi shuttle intrakampus **Institut Teknologi Bandung (ITB) Kampus Jatinangor** berbasis Python yang terinspirasi dari aplikasi **Metro Jabar Trans**. Proyek ini dikembangkan untuk memenuhi Tugas Besar mata kuliah **WI1102 Berpikir Komputasional (Berkom)**.



# Fitur Utama
1. **Peta Kampus Interaktif ITB Jatinangor**
   * Menampilkan denah ITB Jatinangor lengkap dengan jalur lintasan serta 3 titik putar balik.
   * Dilengkapi pin bernomor **`1` – `10`** untuk menandai seluruh titik pemberhentian resmi shuttle.
2. **Simulasi 2 Armada dengan Sistem Anti-Berpapasan**
   * Memantau 2 unit shuttle aktif (**`ITB-01`** dan **`ITB-02`**) secara bersamaan.
   * Menerapkan mekanisme *Phase-Locked Offset* (selisih fase 50%), *Headway Governor*, dan *Two-Way Corridor Lock* pada ruas jalan dua arah agar kedua shuttle tidak saling menyusul maupun berpapasan di jalur sempit.
   * Tersedia tombol pengaturan kecepatan simulasi yaitu **`Simulasi 15x`** / **`Real-time 1x`**.
3. **Estimasi Waktu Penjemputan (ETA)**
   * Pengguna dapat memilih titik penjemputan dan tujuan melalui *dropdown*, tombol tukar rute, atau mengklik langsung daftar halte.
   * Menghitung estimasi waktu kedatangan shuttle terdekat (dalam menit) beserta sisa titik pemberhentian yang harus dilewati.
4. **Informasi Jam Operasional**
   * Menampilkan status layanan secara *real-time* (**`BEROPERASI`** / **`DI LUAR JAM OPERASIONAL`**) berdasarkan jadwal operasional kampus yakni `06:45 – 16:00 WIB`.



# Daftar Titik Pemberhentian
**1**  Halte Gerbang Utama
**2**  Halte Lab. Teknik 1A dan Lab. Teknik 1B
**3**  Halte Gedung Kuliah Umum II dan Lab. Terpadu
**4**  Halte Gedung Kuliah Umum I 
**5**  Halte Gedung Kuliah Umum III dan KOICA
**6**  Halte Asrama TB1 – TB4
**7**  Halte GOR dan GSG
**8**  Halte Gedung Rektorat
**9**  Halte Sekretariat Himpunan & TPA
**10** Halte SITH Kehutanan & Asrama Dosen



# Struktur Folder Proyek

```text
Proyek-Aplikasi-Tracker-Shuttle-Intrakampus-ITB/
├── assets/
│   └── peta_itb_jatinangor.png   # Gambar denah resmi ITB Jatinangor
├── data/
│   ├── __init__.py
│   └── shuttle_data.py           # Data jam operasional, koordinat rute, & 10 titik halte
├── services/
│   ├── __init__.py
│   └── fleet_engine.py           # Engine pergerakan 2 shuttle, anti-berpapasan, & hitung ETA
├── ui/
│   ├── __init__.py
│   ├── map_view.py               # Komponen peta interaktif & canvas rute Merah-Kuning-Biru
│   └── home_view.py              # Antarmuka halaman beranda (tema Biru-Putih ITB)
├── main.py                       # Entry point aplikasi & loop simulasi
├── requirements.txt              # Daftar dependensi library Python
└── README.md

```



# Cara Instalasi & Menjalankan Aplikasi

# Requirements
* **Python 3.10** atau versi lebih baru
* Library **Flet** (`flet>=0.80.0`)

### Langkah-Langkah
1. **Clone repositori**
```bash
git clone [https://github.com/leleglowing/Proyek-Aplikasi-Tracker-Shuttle-Intrakampus-ITB.git](https://github.com/leleglowing/Proyek-Aplikasi-Tracker-Shuttle-Intrakampus-ITB.git)
cd Proyek-Aplikasi-Tracker-Shuttle-Intrakampus-ITB

```
2. **Instal requirements**
```bash
python -m pip install -r requirements.txt

```
*(atau jalankan `python -m pip install flet`)*
3. **Jalankan aplikasi:**
```bash
python main.py

```


## Keterangan

* **Bahasa Pemrograman:** Python
* **UI Framework:** [Flet](https://flet.dev/) (Flutter for Python)
* **Desain & Palet Warna:** Tema Biru ITB (`#00529B`) & Putih bersih



## Anggota Kelompok

* 19626021 - Aurellia Kirana Dewi
* 19626075 - Ganis Lestari Putri
* 19626087 - Aqila Mazaya Vahma
* 19626093 - Teresa Karen Huidinata
* 19626183 - Naurah Adani Busyra

```
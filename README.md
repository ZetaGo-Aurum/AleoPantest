# Aleopantest V3.0 (Major Patch) - Framework Penetration Testing Tingkat Lanjut
<div style="font-size: 80%; color: #666666;">oleh Aleocrophic</div>

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🛡️  Aleopantest V3.0.0 - oleh Aleocrophic  🛡️         ║
║                                                               ║
║              Suite Alat Keamanan Siber Canggih                ║
║                                                               ║
║      400+ Alat • Multi-Platform • TUI Modern • V3.0.0 PRO     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

**Aleopantest** (oleh Aleocrophic) adalah framework penetration testing modular tingkat lanjut yang dirancang untuk profesional keamanan dan ethical hacker. Versi 3.3.5 memperkenalkan dashboard TUI modern, otomasi cerdas, dan dukungan lintas platform yang ditingkatkan.

---

## � Deskripsi Proyek

Aleopantest adalah solusi komprehensif untuk pengujian keamanan yang mencakup berbagai fase pengetesan, mulai dari pengumpulan informasi (reconnaissance) hingga eksploitasi dan pelaporan. Dengan arsitektur plugin-based, pengguna dapat dengan mudah menambahkan alat baru atau mengintegrasikan alat yang sudah ada ke dalam alur kerja yang terotomasi.

### Fitur Utama:
- **Arsitektur Modular**: Mudah diperluas dan dipelihara.
- **CLI Interaktif**: Antarmuka pengguna yang ramah dengan auto-completion dan output yang kaya (Rich output).
- **Lintas Platform**: Berjalan di Windows, Linux, dan macOS.
- **Otomasi Cerdas**: Pengisian parameter berbasis konteks dan optimasi performa.
- **Output Standar**: Pelaporan JSON yang konsisten untuk lebih dari 400 alat.

---

## ⚡ Panduan Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- Pip (Python Package Installer)
- Git (opsional, untuk klon repositori)

### Instalasi Standar
```bash
# Klon repositori
git clone https://github.com/ZetaGo-Aurum/aleopantest.git
cd aleopantest

# Instal dependensi
pip install -r requirements.txt

# Instal sebagai alat CLI (direkomendasikan)
pip install -e .
```

---

## ⚙️ Petunjuk Konfigurasi

Aleopantest menggunakan file konfigurasi untuk mengatur perilaku framework dan integrasi API pihak ketiga.

### 1. File `.env`
Salin file `.env.example` menjadi `.env` dan isi kunci API yang diperlukan:
```env
SHODAN_API_KEY=your_key_here
CENSYS_ID=your_id
CENSYS_SECRET=your_secret
VIRUSTOTAL_API_KEY=your_key
```

### 2. Konfigurasi YAML (`config/default.yml`)
Anda dapat menyesuaikan pengaturan default seperti timeout, user-agent, dan path output di file ini:
```yaml
network:
  timeout: 30
  max_retries: 3
  user_agent: "Aleopantest/3.3.5"
output:
  format: json
  directory: ./results
```

---

## 🎮 Contoh Penggunaan

### Perintah Dasar CLI
```bash
aleopantest --help          # Menampilkan menu bantuan
aleopantest list-tools      # Daftar semua alat yang tersedia
aleopantest info            # Menampilkan info sistem
```

### Menjalankan Alat (CLI)
```bash
# Pemindaian SQL Injection
aleopantest run sql-inject --url http://example.com

# Deteksi Phishing
aleopantest run web-phishing --url http://suspicious-site.com
```

### Penggunaan sebagai Library Python
Anda juga dapat mengintegrasikan modul Aleopantest ke dalam skrip Python Anda sendiri:

```python
from aleopantest.core.scanner import SecurityScanner

# Inisialisasi scanner
scanner = SecurityScanner()

# Jalankan scan pada target
results = scanner.scan_target("http://example.com", modules=["sql_inject", "xss"])

# Cetak hasil
for issue in results.vulnerabilities:
    print(f"Ditemukan: {issue.name} pada {issue.location}")
```

---

## ⚖️ Terms of Service (ToS)

Penggunaan **Aleopantest** diatur oleh ketentuan hukum berikut. Dengan menggunakan perangkat lunak ini, Anda dianggap telah menyetujui seluruh poin di bawah ini.

### 1. Ketentuan Penggunaan
- Aleopantest dikembangkan **eksklusif untuk tujuan edukasi, riset keamanan, dan ethical hacking**.
- Dilarang keras menggunakan alat ini pada sistem atau jaringan tanpa **izin tertulis yang eksplisit** dari pemilik sistem.
- Pengguna bertanggung jawab penuh atas segala aktivitas yang dilakukan menggunakan alat ini.

### 2. Pembatasan Tanggung Jawab
- Pengembang dan kontributor **TIDAK BERTANGGUNG JAWAB** atas penyalahgunaan, aktivitas ilegal, atau kerusakan yang disebabkan oleh perangkat lunak ini.
- Perangkat lunak ini disediakan "APA ADANYA" (AS IS) tanpa jaminan apa pun, baik tersurat maupun tersirat.
- Dalam hal apa pun, penulis tidak bertanggung jawab atas klaim, kerusakan, atau kewajiban lainnya yang timbul dari penggunaan perangkat lunak ini.

### 3. Kebijakan Privasi
- Aleopantest **tidak mengumpulkan atau mengirimkan data pribadi** pengguna ke server luar.
- Seluruh hasil pemindaian dan data sensitif yang dikumpulkan selama pengujian disimpan secara lokal di perangkat pengguna.
- Pengguna bertanggung jawab penuh atas penanganan data yang mereka kumpulkan selama proses penetration testing sesuai dengan regulasi privasi yang berlaku (seperti GDPR atau UU PDP).

### 4. Persyaratan Hak Cipta
- Aleopantest adalah perangkat lunak open-source yang dilisensikan di bawah **Lisensi MIT**.
- Hak cipta (c) 2024 Tim Aleocrophic.
- Anda diperbolehkan menyalin, memodifikasi, dan mendistribusikan perangkat lunak ini selama menyertakan pemberitahuan hak cipta dan izin yang asli.

---

## 🤝 Kontribusi

Kontribusi sangat dihargai! Jika Anda ingin berkontribusi:
1. Fork repositori ini.
2. Buat branch fitur baru (`git checkout -b fitur-baru`).
3. Commit perubahan Anda (`git commit -m 'Menambahkan fitur baru'`).
4. Push ke branch tersebut (`git push origin fitur-baru`).
5. Buat Pull Request.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE).

---
**Aleopantest V3.0.0**
<div style="font-size: 80%; color: #666666;">oleh Aleocrophic</div>

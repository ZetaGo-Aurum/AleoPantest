# Perbaikan Error NoneType pada Aleopantest

## Masalah
Ditemukan error `AttributeError` ketika mengakses atribut nested pada instance tool di `aleopantest/cli.py`, khususnya pada baris 270: `instance.metadata.category.value`. Error ini terjadi jika `metadata` atau `category` bernilai `None`.

## Solusi Implementasi
Telah diimplementasikan solusi komprehensif untuk menangani akses atribut yang tidak aman:

1.  **Fungsi Utilitas `get_safe_attr`**:
    *   Menambahkan fungsi `get_safe_attr(obj, attr_path, default)` di `aleopantest/core/tool_helper.py`.
    *   Fungsi ini secara rekursif menelusuri path atribut (misal: `metadata.category.value`).
    *   Menangani objek (menggunakan `getattr`) dan dictionary (menggunakan `.get()`).
    *   Mengembalikan nilai default jika ada bagian dari path yang bernilai `None` atau tidak ditemukan.

2.  **Pembaruan CLI**:
    *   Memperbarui `aleopantest/cli.py` untuk menggunakan `get_safe_attr` di perintah `info` dan `list-tools`.
    *   Menambahkan blok `try-except` tambahan di sekitar instansiasi tool untuk menangkap error yang mungkin terjadi saat inisialisasi tool itu sendiri.

3.  **Logging**:
    *   Menambahkan logging yang informatif menggunakan `logger.error` untuk mencatat tool mana yang gagal dimuat atau dianalisis.
    *   Logging debug di `get_safe_attr` untuk membantu penelusuran masalah akses atribut di masa mendatang.

4.  **Verifikasi**:
    *   Membuat unit test di `tests/test_safe_attr.py` yang mencakup berbagai kasus edge case (objek None, atribut nested None, dictionary access).
    *   Menjalankan perintah CLI secara manual untuk memastikan tidak ada regresi.

## File yang Dimodifikasi
*   [tool_helper.py](file:///c:/Users/rayhan/Documents/PantestTool/AloPantest/aleopantest/core/tool_helper.py): Menambahkan fungsi `get_safe_attr`.
*   [cli.py](file:///c:/Users/rayhan/Documents/PantestTool/AloPantest/aleopantest/cli.py): Menggunakan `get_safe_attr` dan menambahkan error handling.
*   [test_safe_attr.py](file:///c:/Users/rayhan/Documents/PantestTool/AloPantest/tests/test_safe_attr.py): File baru untuk unit testing.

## Cara Verifikasi
Jalankan unit test:
```bash
python -m unittest tests/test_safe_attr.py
```

Jalankan perintah CLI:
```bash
python aleopantest.py info
python aleopantest.py list-tools
```

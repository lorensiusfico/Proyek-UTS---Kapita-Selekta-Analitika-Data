# Proyek UTS Kapita Selekta Analitika Data
**📚 Library Management API (FastAPI)**

---
## 🚀 Fitur Utama
- **Admin**
  - Menambah, memperbarui, dan menghapus buku.
  - Melihat daftar pinjaman aktif & keterlambatan (*overdue*).
- **Mahasiswa**
  - Melihat buku tersedia.
  - Meminjam buku, memperpanjang masa pinjam, mengembalikan buku.
  - Melihat detail loan milik sendiri, membayar denda setelah pengembalian.
- **Otomatisasi Sistem**
  - Stok otomatis berkurang saat pinjam & bertambah saat kembali.
  - Validasi total durasi ≤ 30 hari dari tanggal pinjam pertama.
  - Denda otomatis, yaitu Rp 5.000 × hari keterlambatan.
  - Denda dibekukan saat return bisa ditandai lunas lewat *endpoint pay*.
- **Debug/QA (admin-only)**
  - Set tanggal jatuh tempo (relative/absolute) agar mudah menguji *overdue* dan denda.
  - Laporan otomatis menghitung ulang denda untuk loan yang belum dikembalikan.
---

## Struktur Folder
```
library_management_api/
├── modules/
│ ├── routes/
│ │ ├── books.py
│ │ ├── loans.py
│ │ └── reports.py
│ ├── schema/
│ │ └── schemas.py
│ └── services/
│ └── services.py
│ └── storage/
│ └── repository.py
│
├── tests/
│ └── test_api.py
│
main.py
.gitignore
README.md 
```
---

## Contoh Endpoint

### Lihat daftar buku
```
GET /books
Headers: { "X-Role": "student", "X-User-Id": "S123" }
```

### Tambah buku (admin)
```
POST /books
Headers: { "X-Role": "admin" }
Body:
{
  "title": "Refactoring",
  "author": "Martin Fowler",
  "year": 2018,
  "stock": 3
}
```

### Pinjam buku
```
POST /loans
Headers: { "X-Role": "student", "X-User-Id": "6162x01xxx" }
Body:
{
  "book_id": "B001",
  "days": 7
}
```

### Perpanjang peminjaman
```
POST /loans/{loan_id}/extend?extra_days=5
Headers: { "X-Role": "student", "X-User-Id": "6162x01xxx" }
```

### Kembalikan buku
```
POST /loans/{loan_id}/return
Headers: { "X-Role": "student", "X-User-Id": "6162x01xxx" }
```

### Bayar Denda
```
POST /loans/{loan_id}/pay
Headers (salah satu):
- Admin:   { "X-Role": "admin" }
- Student: { "X-Role": "student", "X-User-Id": "6162x01xxx" }  # pemiliknya
```

### Laporan admin
```
GET /reports/active-loans
GET /reports/overdue
Headers: { "X-Role": "admin" }
```
Untuk debug, melihat denda bekerja atau tidak
```
POST /reports/_debug/set-due/{loan_id}?days_ago=3
Headers: { "X-Role": "admin" }
```
---
Setelah itu, tes dijalankan menggunakan
```
pytest -q
```
Test utama mencakup:
- CRUD buku (admin)
- Akses role validation
- Pinjam / perpanjang / kembalikan buku
- Perpanjangan > 30 hari → ditolak
- Buku stok 0 → ditolak
- Perhitungan denda keterlambatan
- Laporan aktif & overdue
- Validasi header X-User-Id

## 👥 Role Akses

| Endpoint | Admin | Student |
|-----------|:------:|:--------:|
| **GET /books** | ✅ | ✅ |
| **POST /books** | ✅ | ❌ |
| **PATCH /books/{id}** | ✅ | ❌ |
| **DELETE /books/{id}** | ✅ | ❌ |
| **POST /loans** | ❌ | ✅ |
| **POST /loans/{loan_id}/extend** | ❌ | ✅ |
| **POST /loans/{loan_id}/return** | ❌ | ✅ |
| **GET /reports/active-loans** | ✅ | ❌ |
| **GET /reports/overdue** | ✅ | ❌ |
| **POST /loans/{loan_id}/pay** | ✅ | ✅ (Untuk mahasiswa peminjam) |
| **POST /reports/_debug/set-due-absolute/{loan_id}** | ✅ | ❌ |

---
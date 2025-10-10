# Proyek UTS Kapita Selekta Analitika Data
**📚 Library Management API (FastAPI)**

## 🚀 Fitur Utama
- **Admin**
  - Menambah, memperbarui, dan menghapus buku.
  - Melihat daftar buku yang sedang dipinjam dan laporan keterlambatan.
- **Mahasiswa**
  - Melihat daftar buku tersedia.
  - Meminjam, memperpanjang, dan mengembalikan buku.
- **Otomatisasi Sistem**
  - Pengurangan stok saat buku dipinjam.
  - Pengembalian stok saat buku dikembalikan.
  - Validasi perpanjangan maksimal **30 hari total**.
  - Perhitungan denda otomatis: **Rp 1000 × jumlah hari keterlambatan**.
  - Riwayat peminjaman tersimpan selama server aktif.

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
Headers: { "X-Role": "student", "X-User-Id": "S001" }
Body:
{
  "book_id": "B001",
  "days": 7
}
```

### Perpanjang peminjaman
```
POST /loans/{loan_id}/extend?extra_days=5
Headers: { "X-Role": "student", "X-User-Id": "S001" }
```

### Kembalikan buku
```
POST /loans/{loan_id}/return
Headers: { "X-Role": "student", "X-User-Id": "S001" }
```

### Laporan admin
```
GET /reports/active-loans
GET /reports/overdue
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

---
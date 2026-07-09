# Hands-On 1 — Dasar Python  (± 45 menit)

> **Cara pakai:** JANGAN salin semua kode sekaligus. Buat **satu sel baru untuk
> setiap langkah**, ketik sendiri, tekan **Shift + Enter**, amati hasil sebelum
> lanjut. Belajar terjadi saat Anda mengetik & melihat error.

**Tujuan:** variabel, tipe, operator, list, dictionary, if/for/while, fungsi, error.
**Buat notebook baru:** `latihan_h1.ipynb`.

---

## Bagian A — Variabel, Tipe, Operator

**Sel 1 — buat variabel**
```python
umur = 25
pendapatan = 8.5      # juta rupiah
nama = 'Budi'
aktif = True
print(umur, pendapatan, nama, aktif)
```

**Sel 2 — cek tipe data**
```python
print(type(umur), type(pendapatan), type(nama), type(aktif))
```
▶ Amati: `int float str bool`.

**Sel 3 — operator hitung**
```python
print(7 + 3, 7 - 3, 7 * 3, 7 / 3)
print(7 // 3, 7 % 3, 2 ** 3)      # bagi bulat, sisa, pangkat
```

**Sel 4 — gabung teks (f-string)**
```python
print(f'{nama} usia {umur} th, pendapatan {pendapatan} juta')
```

**Sel 5 — operator perbandingan (hasil boolean)**
```python
print(umur > 20, pendapatan == 8.5, nama != 'Ani')
```
▶ Amati: `True True True`. Ini dasar filter data nanti.

**Sel 6 — (sengaja error) lupa kutip**
```python
kota = Jakarta
```
▶ Amati `NameError`. **Perbaiki** → `kota = 'Jakarta'`. Teks WAJIB pakai kutip.

---

## Bagian B — List

**Sel 7 — buat list & panjang**
```python
angka = [10, 20, 30]
print(angka, len(angka))
```

**Sel 8 — akses (INDEX MULAI 0!)**
```python
print(angka[0], angka[-1])   # pertama, terakhir
```

**Sel 9 — slicing & append**
```python
angka.append(40)
print(angka, angka[1:3])
```

**Sel 10 — ubah & hapus**
```python
angka[0] = 99
angka.remove(40)
print(angka)
```

**Sel 11 — list comprehension (bikin list dari list)**
```python
kuadrat = [x ** 2 for x in [1, 2, 3, 4]]
print(kuadrat)                       # [1, 4, 9, 16]
genap = [x for x in range(10) if x % 2 == 0]
print(genap)                         # [0,2,4,6,8]
```
▶ Amati: cara ringkas & sangat sering dipakai di analisis data.

---

## Bagian C — Dictionary & Tabel Mini

**Sel 12 — dict buat & akses**
```python
nasabah = {'nama': 'Budi', 'umur': 25, 'pendapatan': 8.5}
print(nasabah['nama'], nasabah['pendapatan'])
```

**Sel 13 — tambah key & lihat isi**
```python
nasabah['kota'] = 'Depok'
print(nasabah.keys())
print(nasabah.values())
```

**Sel 14 — list of dict = tabel mini (cikal bakal DataFrame)**
```python
data = [
    {'nama': 'Budi', 'dbr': 0.55},
    {'nama': 'Ani',  'dbr': 0.30},
    {'nama': 'Cici', 'dbr': 0.70},
]
for row in data:
    print(row['nama'], row['dbr'])
```

---

## Bagian D — Kondisi, Perulangan, Fungsi

**Sel 15 — if / elif / else**
```python
dbr = 0.55
if dbr > 0.6:
    print('TINGGI')
elif dbr > 0.4:
    print('SEDANG')
else:
    print('AMAN')
```

**Sel 16 — for menjumlahkan**
```python
total = 0
for n in [10, 20, 30]:
    total += n
print('Total:', total)   # 60
```

**Sel 17 — while (ulang selama syarat benar)**
```python
saldo = 100
bulan = 0
while saldo > 0:
    saldo -= 30
    bulan += 1
print('Habis dalam', bulan, 'bulan')
```

**Sel 18 — buat fungsi sendiri**
```python
def klasifikasi_dbr(d):
    if d > 0.6:
        return 'TINGGI'
    elif d > 0.4:
        return 'SEDANG'
    return 'AMAN'

print(klasifikasi_dbr(0.55), klasifikasi_dbr(0.2))
```
▶ Amati: fungsi = rumus yang bisa dipakai berulang.

**Sel 19 — pakai fungsi pada tabel mini**
```python
for row in data:
    print(row['nama'], '->', klasifikasi_dbr(row['dbr']))
```

**Sel 20 — try/except (tangani error dengan anggun)**
```python
try:
    hasil = 10 / 0
except ZeroDivisionError:
    print('Tidak bisa bagi nol')
```

---

## Latihan Mandiri

1. `pendapatan_tim = [7.5, 9.0, 12.0, 6.5]` → cetak jumlah, rata-rata, maks, min.
2. Buat dict `saya` (nama, umur, kota). Cetak perkenalan pakai f-string.
3. List comprehension: dari `[0.3,0.65,0.5,0.8,0.2]` buat list `True/False` untuk >0.5.
4. Buat fungsi `lulus(nilai)` → 'LULUS' bila ≥60, else 'REMEDIAL'. Uji 3 nilai.
5. Pakai `while` untuk hitung berapa kali 1.000.000 harus dibagi 2 sampai < 1.000.
6. Hitung berapa nasabah pada `data` (Sel 14) yang DBR-nya 'TINGGI' (for + fungsi).

---

## 🏁 Tantangan 45 Menit (mini-project)

Buat "kalkulator kelayakan pinjaman sederhana":
1. Buat list of dict berisi **5 pemohon** (nama, pendapatan_juta, cicilan_juta).
2. Buat fungsi `hitung_dbr(pendapatan, cicilan)` → kembalikan rasio.
3. Buat fungsi `keputusan(dbr)` → 'DISETUJUI' bila DBR < 0.4, 'REVIEW' bila
   0.4–0.6, 'DITOLAK' bila > 0.6.
4. Loop semua pemohon, cetak: nama, DBR (2 desimal), keputusan.
5. Hitung berapa yang DISETUJUI.

✅ **Selesai bila:** Anda bisa membuat variabel/list/dict, if/for/while, fungsi,
dan menyelesaikan mini-project tanpa menyalin.

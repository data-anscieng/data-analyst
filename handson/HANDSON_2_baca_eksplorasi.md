# Hands-On 2 — Baca Excel & Eksplorasi Data  (± 45 menit)

> Satu sel per langkah. Ketik sendiri, Shift+Enter, amati.

**Tujuan:** memuat Excel, mengenali isi data, menyaring, mengurutkan, meringkas cepat.
**Data:** `data/nasabah_loan.xlsx` (2008 baris — DUMMY).
**Buat notebook:** `latihan_h2.ipynb` (di folder yang sama dengan folder `data/`).

---

## Bagian A — Memuat Data

**Sel 1 — impor pandas**
```python
import pandas as pd
```

**Sel 2 — cek lokasi kerja (kalau file tak ketemu)**
```python
import os
print(os.getcwd())
os.listdir('data')[:5]
```

**Sel 3 — baca Excel**
```python
df = pd.read_excel('data/nasabah_loan.xlsx')
df.head()
```

**Sel 4 — ukuran & kolom**
```python
print('Baris, kolom:', df.shape)
print(df.columns.tolist())
```

**Sel 5 — baca hanya kolom tertentu**
```python
kecil = pd.read_excel('data/nasabah_loan.xlsx',
                      usecols=['nasabah_id', 'pendapatan_juta', 'dbr'])
kecil.head()
```
▶ Amati: berguna untuk file besar — muat seperlunya.

**Sel 6 — intip acak & ekor**
```python
df.tail(3)
df.sample(5)
```

---

## Bagian B — Mengenali Data

**Sel 7 — info tipe & non-kosong**
```python
df.info()
```

**Sel 8 — statistik ringkas (= Descriptive Statistics Excel)**
```python
df.describe()
```

**Sel 9 — ringkasan satu kolom**
```python
print('Rata-rata DBR :', df['dbr'].mean().round(3))
print('Median income:', df['pendapatan_juta'].median())
print('Maks pinjaman :', df['jumlah_pinjaman_juta'].max())
```

**Sel 10 — hitung kategori (= COUNTIF)**
```python
df['pekerjaan'].value_counts()
```

**Sel 11 — proporsi kategori**
```python
df['wilayah'].value_counts(normalize=True).round(3)
```

**Sel 12 — cek nilai kosong**
```python
df.isna().sum()
```

**Sel 13 — tabel silang 2 kategori (crosstab)**
```python
pd.crosstab(df['pekerjaan'], df['wilayah'])
```
▶ Amati: jumlah nasabah per kombinasi pekerjaan × wilayah.

---

## Bagian C — Filter, Sort, Ranking

**Sel 14 — filter satu syarat**
```python
beban_tinggi = df[df['dbr'] > 0.4]
print(beban_tinggi.shape[0], 'nasabah DBR > 0.4')
```

**Sel 15 — filter dua syarat (kurung wajib!)**
```python
muda_beban = df[(df['usia'] < 30) & (df['dbr'] > 0.5)]
muda_beban.head()
```

**Sel 16 — filter rentang (between) & isin**
```python
df[df['usia'].between(30, 40)].shape
df[df['pekerjaan'].isin(['Wiraswasta', 'Profesional'])].shape
```

**Sel 17 — urutkan & ranking cepat**
```python
df.nlargest(5, 'jumlah_pinjaman_juta')[['nasabah_id', 'jumlah_pinjaman_juta', 'dbr']]
df.nsmallest(5, 'pendapatan_juta')[['nasabah_id', 'pendapatan_juta']]
```

**Sel 18 — pilih kolom + query()**
```python
df.query('usia < 30 and dbr > 0.5').shape
```

---

## Bagian D — Ringkas & Simpan

**Sel 19 — buat kolom bantu & ringkas**
```python
df['default_txt'] = df['status_default'].map({0: 'Lancar', 1: 'Default'})
df['default_txt'].value_counts()
```

**Sel 20 — simpan hasil filter**
```python
beban_tinggi.to_excel('beban_tinggi.xlsx', index=False)
print('Tersimpan: beban_tinggi.xlsx')
```

---

## Latihan Mandiri

1. Berapa banyak nasabah dari `wilayah == 'Jabodetabek'`?
2. Tampilkan 10 pinjaman terbesar + kolom `nasabah_id`, `pekerjaan`, `dbr`.
3. Rata-rata `dbr` nasabah `pekerjaan == 'Wiraswasta'`.
4. Berapa % nasabah dengan `dpd_max > 30`? (`(df['dpd_max']>30).mean()`)
5. Crosstab `pekerjaan` × `default_txt` — pekerjaan mana default-nya paling banyak?
6. Nasabah usia 25–35 DAN pendapatan > 15 juta: berapa banyak?
7. Simpan nasabah usia < 25 ke `nasabah_muda.csv`.

---

## 🏁 Tantangan 45 Menit — "Profil Portofolio 1 Halaman"

Buat ringkasan portofolio nasabah dalam beberapa sel:
1. Total nasabah, rata-rata pendapatan, rata-rata DBR, default rate keseluruhan.
2. Top-3 wilayah dengan nasabah terbanyak.
3. Pekerjaan dengan DBR rata-rata tertinggi.
4. Persentase nasabah "berisiko" (DBR > 0.5 ATAU dpd_max > 30).
5. Kumpulkan semua angka ke satu `dict` bernama `ringkasan`, lalu ubah jadi
   DataFrame 1 baris dan simpan ke `profil_portofolio.csv`.

✅ **Selesai bila:** Anda bisa memuat, mengeksplor, menyaring, meringkas data dan
menghasilkan file profil portofolio.

# Hands-On 3 — GroupBy (PivotTable) + Cleaning  (± 45 menit)

> Satu sel per langkah. Ketik sendiri, Shift+Enter, amati.

**Tujuan:** ringkas per kelompok (groupby & pivot_table), gabung tabel (merge),
bersihkan NaN & duplikat, buat kolom baru, binning.
**Data:** `data/nasabah_loan.xlsx`.
**Buat notebook:** `latihan_h3.ipynb`.

---

## Bagian A — Muat & Periksa Kualitas

**Sel 1**
```python
import pandas as pd
import numpy as np
df = pd.read_excel('data/nasabah_loan.xlsx')
print(df.shape)
```

**Sel 2 — cek tipe data**
```python
df.dtypes
```

**Sel 3 — cek duplikat & kosong**
```python
print('Duplikat:', df.duplicated().sum())
print(df.isna().sum())
```

---

## Bagian B — Cleaning

**Sel 4 — buang duplikat**
```python
df = df.drop_duplicates()
print('Baris setelah drop:', df.shape[0])
```

**Sel 5 — lihat baris kosong**
```python
df[df['pendapatan_juta'].isna()].head()
```

**Sel 6 — isi kosong dengan median**
```python
for kol in ['pendapatan_juta', 'lama_kerja_thn']:
    df[kol] = df[kol].fillna(df[kol].median())
df.isna().sum().sum()      # harus 0
```

**Sel 7 — rapikan teks kategori**
```python
df['wilayah'] = df['wilayah'].str.strip().str.title()
df['wilayah'].unique()
```

---

## Bagian C — GroupBy (= PivotTable)

**Sel 8 — rata-rata DBR per wilayah**
```python
df.groupby('wilayah')['dbr'].mean().sort_values(ascending=False)
```

**Sel 9 — default rate per wilayah**
```python
default_wil = df.groupby('wilayah')['status_default'].mean().sort_values(ascending=False)
default_wil
```

**Sel 10 — beberapa agregasi sekaligus**
```python
df.groupby('pekerjaan').agg(
    jumlah=('nasabah_id', 'count'),
    dbr_rata=('dbr', 'mean'),
    income_median=('pendapatan_juta', 'median'),
).round(2)
```

**Sel 11 — groupby dua kolom**
```python
df.groupby(['wilayah', 'pekerjaan'])['dbr'].mean().round(3).head(10)
```

**Sel 12 — pivot_table (persis PivotTable Excel)**
```python
df.pivot_table(index='wilayah', columns='pekerjaan',
               values='status_default', aggfunc='mean').round(3)
```
▶ Amati: baris=wilayah, kolom=pekerjaan, nilai=default rate. Ini PivotTable murni.

---

## Bagian D — Kolom Baru, Binning, Merge

**Sel 13 — kolom baru dengan kondisi**
```python
df['kelas_dbr'] = np.where(df['dbr'] > 0.5, 'Tinggi', 'Aman')
df['beban_setahun'] = df['cicilan_juta'] * 12
df[['dbr', 'kelas_dbr', 'beban_setahun']].head()
```

**Sel 14 — binning usia (pd.cut)**
```python
df['kelompok_usia'] = pd.cut(df['usia'], bins=[0, 30, 45, 100],
                             labels=['Muda', 'Dewasa', 'Senior'])
df['kelompok_usia'].value_counts()
```

**Sel 15 — apply lambda (kolom turunan bebas)**
```python
df['income_per_tanggungan'] = df.apply(
    lambda r: r['pendapatan_juta'] / (r['jumlah_tanggungan'] + 1), axis=1)
df[['pendapatan_juta', 'jumlah_tanggungan', 'income_per_tanggungan']].head()
```

**Sel 16 — default rate per kelompok usia**
```python
df.groupby('kelompok_usia', observed=True)['status_default'].mean().round(3)
```

**Sel 17 — jumlah nasabah per wilayah (untuk digabung)**
```python
per_wil = df.groupby('wilayah').size().reset_index(name='jumlah_nasabah')
per_wil
```

**Sel 18 — merge dua tabel ringkasan**
```python
ringkas = per_wil.merge(default_wil.reset_index(), on='wilayah')
ringkas = ringkas.sort_values('status_default', ascending=False)
ringkas
```

**Sel 19 — simpan**
```python
ringkas.to_csv('ringkasan_wilayah.csv', index=False)
df.to_excel('nasabah_bersih.xlsx', index=False)   # dipakai H4/H8/H9
print('Tersimpan: ringkasan_wilayah.csv & nasabah_bersih.xlsx')
```

---

## Latihan Mandiri

1. Rata-rata `beban_setahun` per pekerjaan?
2. Wilayah dengan default rate tertinggi & terendah?
3. Kelompok usia mana paling berisiko (default rate tertinggi)?
4. pivot_table: index=`kelompok_usia`, columns=`kelas_dbr`, nilai=default rate.
5. GroupBy `pekerjaan`, hitung **jumlah** & **proporsi** nasabah default.
6. Buat kolom `layak` = 'Ya' bila DBR<0.4 dan dpd_max<15, else 'Tidak'. Berapa 'Ya'?
7. Simpan pivot_table default rate wilayah×pekerjaan ke `pivot_default.csv`.

---

## 🏁 Tantangan 45 Menit — "Tabel Risiko Wilayah"

1. Bangun satu tabel per **wilayah** berisi: jumlah nasabah, income median,
   DBR rata-rata, default rate, % nasabah kelas DBR 'Tinggi'.
2. Urutkan dari default rate tertinggi.
3. Tambah kolom `prioritas` = 'Awasi' bila default rate > rata-rata nasional, else 'Aman'.
4. Simpan ke `tabel_risiko_wilayah.xlsx`.
5. Tulis 2 kalimat kesimpulan (sebagai komentar `#`) tentang wilayah paling berisiko.

✅ **Selesai bila:** data bersih + Anda bisa membuat pivot/groupby/merge dan
menghasilkan tabel risiko wilayah.

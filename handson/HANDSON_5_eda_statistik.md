# Hands-On 6 — EDA & Statistik Deskriptif  (± 45 menit)

> Satu sel per langkah. Ketik sendiri, Shift+Enter, amati.

**Tujuan:** menggali data secara sistematis (Exploratory Data Analysis): ukuran
pemusatan & sebaran, persentil, deteksi outlier (IQR), korelasi, profiling.
**Data:** `data/nasabah_loan.xlsx`.
**Buat notebook:** `latihan_h6.ipynb`.

---

## Bagian A — Ringkasan Menyeluruh

**Sel 1 — muat & bersihkan**
```python
import pandas as pd
import numpy as np
df = pd.read_excel('data/nasabah_loan.xlsx').drop_duplicates()
for k in ['pendapatan_juta', 'lama_kerja_thn']:
    df[k] = df[k].fillna(df[k].median())
df.shape
```

**Sel 2 — ringkasan angka & kategori**
```python
df.describe()                        # kolom numerik
```

**Sel 3 — ringkasan kolom kategori**
```python
df.describe(include='object')        # count, unique, top, freq
```

**Sel 4 — ukuran pemusatan & sebaran satu kolom**
```python
kol = 'pendapatan_juta'
print('mean  :', round(df[kol].mean(), 2))
print('median:', round(df[kol].median(), 2))
print('std   :', round(df[kol].std(), 2))
print('range :', round(df[kol].max() - df[kol].min(), 2))
```
▶ Amati: mean > median → distribusi miring ke kanan.

---

## Bagian B — Bentuk Distribusi & Persentil

**Sel 5 — skewness & kurtosis**
```python
print('skew    :', round(df[kol].skew(), 2))     # >0 = ekor kanan
print('kurtosis:', round(df[kol].kurt(), 2))     # >0 = ekor tebal
```

**Sel 6 — persentil (quantile)**
```python
df[kol].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).round(2)
```
▶ Amati: 90% nasabah berpendapatan di bawah nilai P90.

---

## Bagian C — Deteksi Outlier (metode IQR)

**Sel 7 — hitung batas IQR**
```python
q1, q3 = df[kol].quantile([0.25, 0.75])
iqr = q3 - q1
batas_atas = q3 + 1.5 * iqr
batas_bawah = q1 - 1.5 * iqr
print('Batas bawah:', round(batas_bawah, 2), '| batas atas:', round(batas_atas, 2))
```

**Sel 8 — cari & hitung outlier**
```python
outlier = df[(df[kol] < batas_bawah) | (df[kol] > batas_atas)]
print('Jumlah outlier:', len(outlier))
outlier[['nasabah_id', kol]].head()
```
▶ Diskusi: outlier income = nasabah kaya (wajar) atau salah input? Jangan asal buang.

---

## Bagian D — Hubungan Antar Variabel

**Sel 9 — matriks korelasi**
```python
num = df.select_dtypes('number')
korelasi = num.corr().round(2)
korelasi['status_default'].sort_values(ascending=False)
```
▶ Amati: variabel mana paling berkorelasi dengan gagal bayar (dbr, dpd_max?).

**Sel 10 — pasangan korelasi terkuat**
```python
c = num.corr().abs()
pasangan = (c.where(~np.eye(len(c), dtype=bool))
              .stack().sort_values(ascending=False))
pasangan.head(5).round(2)
```

**Sel 11 — statistik per kelompok (groupby describe)**
```python
df.groupby('pekerjaan')['pendapatan_juta'].describe().round(1)
```

---

## Bagian E — Crosstab & Profiling Otomatis

**Sel 12 — crosstab proporsi (baris = 100%)**
```python
pd.crosstab(df['pekerjaan'], df['status_default'], normalize='index').round(3)
```
▶ Amati: proporsi default per pekerjaan.

**Sel 13 — binning + default rate per bin income**
```python
df['bin_income'] = pd.qcut(df['pendapatan_juta'], q=4,
                           labels=['Q1', 'Q2', 'Q3', 'Q4'])
df.groupby('bin_income', observed=True)['status_default'].mean().round(3)
```
▶ Amati: apakah income lebih tinggi → default lebih rendah?

**Sel 14 — fungsi profiling ringkas (dipakai berulang)**
```python
def profil(data):
    return pd.DataFrame({
        'tipe': data.dtypes.astype(str),
        'kosong': data.isna().sum(),
        'unik': data.nunique(),
    })
profil(df)
```

**Sel 15 — simpan ringkasan EDA**
```python
num.describe().T.to_csv('eda_ringkasan.csv')
print('Tersimpan: eda_ringkasan.csv')
```

---

## Latihan Mandiri

1. Skewness `dbr` dan `jumlah_pinjaman_juta` — mana paling miring?
2. Hitung outlier `dbr` dengan metode IQR. Berapa banyak?
3. Variabel apa paling berkorelasi (positif & negatif) dengan `dpd_max`?
4. Groupby `wilayah`: statistik `pendapatan_juta` (describe). Wilayah mana paling makmur?
5. Crosstab `kelompok pekerjaan` × default (normalize) — pekerjaan mana paling berisiko?
6. Buat kuartil `dbr` (qcut) dan lihat default rate tiap kuartil.

---

## 🏁 Tantangan 45 Menit — "Laporan EDA Otomatis"

Bangun mini-laporan EDA dalam beberapa sel:
1. Fungsi `profil()` untuk struktur data (tipe, kosong, unik).
2. Statistik deskriptif semua kolom numerik + skewness.
3. Deteksi outlier untuk 3 kolom kunci (income, dbr, jumlah_pinjaman) via IQR.
4. Top-5 pasangan variabel paling berkorelasi.
5. Tabel default rate per kuartil income & per pekerjaan.
6. Simpan semua tabel ke `laporan_eda.xlsx` (multi-sheet) + tulis 3 temuan (`#`).

✅ **Selesai bila:** Anda bisa meringkas data (pemusatan/sebaran/persentil),
mendeteksi outlier, membaca korelasi, dan menghasilkan laporan EDA.

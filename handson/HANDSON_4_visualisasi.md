# Hands-On 4 — Visualisasi Data  (± 45 menit)

> Satu sel per langkah. Ketik sendiri, Shift+Enter, amati grafik.

**Tujuan:** histogram, bar, box, violin, scatter, countplot, heatmap, lineplot,
subplot; styling; simpan PNG.
**Data:** `data/nasabah_loan.xlsx`.
**Buat notebook:** `latihan_h4.ipynb`.

---

## Bagian A — Persiapan

**Sel 1 — impor & muat + bersihkan cepat**
```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel('data/nasabah_loan.xlsx').drop_duplicates()
df['pendapatan_juta'] = df['pendapatan_juta'].fillna(df['pendapatan_juta'].median())
df['kelas_dbr'] = np.where(df['dbr'] > 0.5, 'Tinggi', 'Aman')
df.shape
```

---

## Bagian B — Distribusi

**Sel 2 — histogram DBR**
```python
sns.histplot(df, x='dbr', bins=30)
plt.title('Distribusi DBR'); plt.xlabel('DBR'); plt.show()
```

**Sel 3 — histogram pendapatan (kemiringan)**
```python
sns.histplot(df, x='pendapatan_juta', bins=40)
plt.title('Distribusi Pendapatan'); plt.show()
```
▶ Amati: miring ke kanan (skewed).

**Sel 4 — histogram + KDE**
```python
sns.histplot(df, x='dbr', bins=30, kde=True)
plt.title('DBR + KDE'); plt.show()
```

---

## Bagian C — Bandingkan Kategori

**Sel 5 — default rate per wilayah (bar)**
```python
default_wil = df.groupby('wilayah')['status_default'].mean().sort_values()
default_wil.plot(kind='barh')
plt.title('Default Rate per Wilayah'); plt.xlabel('Proporsi'); plt.show()
```

**Sel 6 — jumlah per pekerjaan**
```python
df['pekerjaan'].value_counts().plot(kind='bar')
plt.title('Jumlah Nasabah per Pekerjaan'); plt.xticks(rotation=0); plt.show()
```

**Sel 7 — countplot dengan hue**
```python
sns.countplot(df, x='pekerjaan', hue='kelas_dbr')
plt.title('Kelas DBR per Pekerjaan'); plt.xticks(rotation=15); plt.show()
```

**Sel 8 — barplot rata-rata (dengan estimator)**
```python
sns.barplot(df, x='pekerjaan', y='pendapatan_juta', estimator='mean')
plt.title('Rata-rata Pendapatan per Pekerjaan'); plt.xticks(rotation=15); plt.show()
```

---

## Bagian D — Sebaran per Grup

**Sel 9 — box pendapatan per pekerjaan**
```python
sns.boxplot(df, x='pekerjaan', y='pendapatan_juta')
plt.title('Pendapatan per Pekerjaan'); plt.xticks(rotation=15); plt.show()
```
▶ Amati: median (garis) & outlier (titik).

**Sel 10 — violin plot (box + kepadatan)**
```python
sns.violinplot(df, x='kelas_dbr', y='pendapatan_juta')
plt.title('Distribusi Pendapatan per Kelas DBR'); plt.show()
```

---

## Bagian E — Hubungan & Korelasi

**Sel 11 — scatter pendapatan vs DBR (warna=default)**
```python
sns.scatterplot(df, x='pendapatan_juta', y='dbr', hue='status_default', alpha=0.5)
plt.title('Pendapatan vs DBR'); plt.show()
```

**Sel 12 — lineplot: rata-rata DBR per usia (tren)**
```python
tren = df.groupby('usia')['dbr'].mean().reset_index()
sns.lineplot(tren, x='usia', y='dbr')
plt.title('Rata-rata DBR per Usia'); plt.show()
```

**Sel 13 — heatmap korelasi**
```python
num = df.select_dtypes('number')
sns.heatmap(num.corr(), annot=False, cmap='Greens')
plt.title('Korelasi Antar Variabel'); plt.show()
```

---

## Bagian F — Dashboard & Simpan

**Sel 14 — 2×2 subplot**
```python
fig, ax = plt.subplots(2, 2, figsize=(12, 8))
sns.histplot(df, x='dbr', ax=ax[0, 0]); ax[0, 0].set_title('DBR')
sns.histplot(df, x='pendapatan_juta', ax=ax[0, 1]); ax[0, 1].set_title('Pendapatan')
default_wil.plot(kind='barh', ax=ax[1, 0]); ax[1, 0].set_title('Default per Wilayah')
sns.boxplot(df, x='kelas_dbr', y='pendapatan_juta', ax=ax[1, 1]); ax[1, 1].set_title('Income per Kelas DBR')
plt.tight_layout(); plt.show()
```

**Sel 15 — simpan dashboard ke PNG**
```python
fig.savefig('dashboard_risiko.png', dpi=150, bbox_inches='tight')
print('Tersimpan: dashboard_risiko.png')
```

---

## Latihan Mandiri

1. Histogram `jumlah_pinjaman_juta` — simetris atau miring?
2. Bar rata-rata `dbr` per pekerjaan.
3. Scatter `usia` vs `pendapatan_juta` diwarnai `pekerjaan`.
4. Violin `dbr` per `pekerjaan`.
5. Dari heatmap, sebutkan 2 variabel paling berkorelasi dengan `dpd_max`.
6. Lineplot rata-rata `pendapatan_juta` per usia.
7. Simpan satu grafik favorit ke PNG dengan judul & label lengkap.

**Prinsip:** tiap grafik WAJIB judul + label. Satu grafik = satu pesan.

---

## 🏁 Tantangan 45 Menit — "Storyboard Risiko"

Susun 4 grafik yang bersama-sama menceritakan **profil risiko nasabah**:
1. Distribusi DBR (histogram).
2. Default rate per wilayah (bar).
3. Pendapatan per kelas DBR (box/violin).
4. Scatter pendapatan vs DBR diwarnai default.
Gabungkan ke satu figure 2×2, beri judul besar `plt.suptitle(...)`, simpan PNG,
lalu tulis 3 temuan utama sebagai komentar `#`.

✅ **Selesai bila:** Anda menghasilkan ≥ 8 grafik berlabel + 1 dashboard PNG.

# Hands-On 8 — Segmentasi Nasabah Loan (K-Means)  (± 45 menit)

> Satu sel per langkah. Ketik sendiri, Shift+Enter, amati.

**Tujuan:** clustering K-Means, pilih k (elbow + silhouette), profil & nama segmen,
visualisasi PCA, aksi bisnis.
**Data:** `data/nasabah_loan.xlsx`.
**Buat notebook:** `latihan_h6.ipynb`.

---

## Bagian A — Siapkan Fitur

**Sel 1 — muat & bersihkan**
```python
import pandas as pd
df = pd.read_excel('data/nasabah_loan.xlsx').drop_duplicates()
for k in ['pendapatan_juta', 'lama_kerja_thn']:
    df[k] = df[k].fillna(df[k].median())
df.shape
```

**Sel 2 — pilih fitur segmentasi**
```python
fitur = ['pendapatan_juta', 'dbr', 'jumlah_pinjaman_juta', 'tenor_bulan', 'usia']
X_raw = df[fitur]
X_raw.head()
```
▶ Kita TIDAK memakai `status_default` (itu untuk klasifikasi).

**Sel 3 — kenapa perlu standardisasi**
```python
X_raw.describe().round(1)
```
▶ Amati: skala `pendapatan_juta` >> `dbr`. Tanpa distandarkan, income mendominasi jarak.

**Sel 4 — standardisasi**
```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(X_raw)
X[:3].round(2)
```

---

## Bagian B — Memilih Jumlah Cluster

**Sel 5 — elbow (inersia) k=2..8**
```python
from sklearn.cluster import KMeans
inersia = []
for k in range(2, 9):
    inersia.append(KMeans(n_clusters=k, random_state=42, n_init=10).fit(X).inertia_)
inersia
```

**Sel 6 — plot elbow**
```python
import matplotlib.pyplot as plt
plt.plot(range(2, 9), inersia, 'o-')
plt.xlabel('k'); plt.ylabel('Inersia'); plt.title('Metode Elbow'); plt.show()
```

**Sel 7 — silhouette (makin tinggi makin baik)**
```python
from sklearn.metrics import silhouette_score
for k in range(2, 7):
    lab = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(X)
    print(k, round(silhouette_score(X, lab), 3))
```
▶ Amati: bandingkan dengan elbow — pilih k yang masuk akal & mudah dinamai.

---

## Bagian C — Segmentasi Final & Profil

**Sel 8 — K-Means final**
```python
km = KMeans(n_clusters=4, random_state=42, n_init=10)
df['segmen'] = km.fit_predict(X)
df['segmen'].value_counts()
```

**Sel 9 — profil tiap segmen**
```python
profil = df.groupby('segmen')[fitur].mean().round(2)
profil
```

**Sel 10 — pusat cluster dikembalikan ke skala asli**
```python
pusat = pd.DataFrame(scaler.inverse_transform(km.cluster_centers_), columns=fitur)
pusat.round(1)
```
▶ Amati: nilai fitur "khas" tiap segmen dalam satuan asli (lebih mudah dibaca).

**Sel 11 — default rate per segmen (konteks bisnis)**
```python
df.groupby('segmen')['status_default'].mean().round(3)
```

**Sel 12 — boxplot fitur per segmen**
```python
import seaborn as sns
sns.boxplot(df, x='segmen', y='dbr'); plt.title('DBR per Segmen'); plt.show()
```

---

## Bagian D — Visualisasi PCA & Penamaan

**Sel 13 — PCA 2D untuk melihat pemisahan cluster**
```python
from sklearn.decomposition import PCA
koord = PCA(n_components=2, random_state=42).fit_transform(X)
df['pc1'], df['pc2'] = koord[:, 0], koord[:, 1]
sns.scatterplot(df, x='pc1', y='pc2', hue='segmen', palette='Set2', alpha=0.6)
plt.title('Segmen (proyeksi PCA 2D)'); plt.show()
```
▶ Amati: apakah segmen terpisah jelas?

**Sel 14 — beri nama segmen (SESUAIKAN dg profil)**
```python
nama = {0: 'Prime', 1: 'Emerging', 2: 'Berisiko', 3: 'Atas'}   # sesuaikan!
df['nama_segmen'] = df['segmen'].map(nama)
df['nama_segmen'].value_counts()
```

**Sel 15 — tabel ringkas per nama segmen**
```python
df.groupby('nama_segmen').agg(
    jumlah=('nasabah_id', 'count'),
    income=('pendapatan_juta', 'mean'),
    dbr=('dbr', 'mean'),
    default_rate=('status_default', 'mean'),
).round(2)
```

**Sel 16 — crosstab segmen × pekerjaan**
```python
pd.crosstab(df['nama_segmen'], df['pekerjaan'])
```

**Sel 17 — simpan**
```python
df[['nasabah_id', 'segmen', 'nama_segmen']].to_csv('segmen_nasabah.csv', index=False)
print('Tersimpan: segmen_nasabah.csv')
```

---

## Latihan Mandiri

1. Ulangi dengan **k=3**. Lebih mudah dinamai?
2. Tulis 1 aksi bisnis per segmen (limit, bunga, penawaran).
3. Tambahkan `jumlah_tanggungan` ke fitur. Profil berubah?
4. Segmen mana punya default rate tertinggi? Cocokkah dengan namanya?
5. Dari PCA, apakah ada segmen yang tumpang tindih? Apa artinya?
6. Segmen mana paling menarik untuk kampanye produk baru? Argumen.

---

## 🏁 Tantangan 45 Menit — "Kartu Segmen Pelanggan"

Untuk tiap segmen bernama, buat "kartu" berisi:
1. Ukuran (jumlah & % dari total).
2. Profil ringkas (income, DBR, usia, pinjaman rata-rata).
3. Tingkat risiko (default rate) → label Rendah/Sedang/Tinggi.
4. **Rekomendasi aksi** (produk/limit/bunga).
Susun semua kartu ke satu DataFrame ringkasan & simpan `kartu_segmen.xlsx`.

✅ **Selesai bila:** Anda punya 4 segmen bernama, profil (termasuk pusat asli &
PCA), dan ≥ 1 aksi bisnis per segmen.

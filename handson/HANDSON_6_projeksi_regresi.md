# Hands-On 7 — Projeksi Pertumbuhan Sektor (Regresi)  (± 45 menit)

> Satu sel per langkah. Ketik sendiri, Shift+Enter, amati.
> **Jembatan STATA:** ini padanan `reg y x` — output `.summary()` kolomnya sama
> dengan tabel regresi STATA.

**Tujuan:** regresi linear (sederhana, log, berganda), baca coef/p-value/R²,
proyeksi, bandingkan model & sektor.
**Data:** `data/penjualan_sektor.csv` (per sektor 2015–2024).
**Buat notebook:** `latihan_h5.ipynb`. **Library:** `statsmodels`, `scikit-learn`.

---

## Bagian A — Muat & Lihat Tren

**Sel 1**
```python
import pandas as pd
sektor = pd.read_csv('data/penjualan_sektor.csv')
sektor.head()
```

**Sel 2 — daftar sektor**
```python
sektor['sektor'].unique()
```

**Sel 3 — pilih satu sektor**
```python
d = sektor[sektor['sektor'] == 'Teknologi'].copy()
d
```

**Sel 4 — lihat tren**
```python
import matplotlib.pyplot as plt
plt.plot(d['tahun'], d['pendapatan_miliar'], marker='o')
plt.title('Pendapatan Sektor Teknologi'); plt.xlabel('Tahun'); plt.show()
```

---

## Bagian B — Regresi Sederhana (gaya STATA)

**Sel 5 — jalankan regresi**
```python
import statsmodels.formula.api as smf
model = smf.ols('pendapatan_miliar ~ tahun', data=d).fit()
model.summary()
```
▶ Bandingkan STATA: **coef tahun** = kenaikan/tahun; **P>|t|**<0.05 = signifikan; **R-squared** = kecocokan.

**Sel 6 — ambil angka penting**
```python
print('Kenaikan/tahun :', round(model.params['tahun'], 2), 'miliar')
print('R-squared      :', round(model.rsquared, 3))
print('p-value tahun  :', round(model.pvalues['tahun'], 4))
```

**Sel 7 — selang kepercayaan koefisien (confidence interval)**
```python
model.conf_int()
```
▶ Amati: rentang kemungkinan nilai koef (ketidakpastian estimasi).

**Sel 8 — bandingkan dengan sklearn (hasil sama?)**
```python
from sklearn.linear_model import LinearRegression
X = d[['tahun']]; y = d['pendapatan_miliar']
lr = LinearRegression().fit(X, y)
print('coef sklearn:', round(lr.coef_[0], 2), '| R2:', round(lr.score(X, y), 3))
```

---

## Bagian C — Projeksi & Diagnostik

**Sel 9 — prediksi 2025–2027**
```python
masa_depan = pd.DataFrame({'tahun': [2025, 2026, 2027]})
masa_depan['proyeksi'] = model.predict(masa_depan)
masa_depan
```

**Sel 10 — grafik data + proyeksi**
```python
plt.plot(d['tahun'], d['pendapatan_miliar'], 'o-', label='Aktual')
plt.plot(masa_depan['tahun'], masa_depan['proyeksi'], 's--', label='Proyeksi')
plt.legend(); plt.title('Proyeksi Sektor Teknologi'); plt.show()
```

**Sel 11 — cek residual**
```python
plt.scatter(d['tahun'], model.resid); plt.axhline(0, color='red')
plt.title('Residual (idealnya acak di sekitar 0)'); plt.show()
```

**Sel 12 — error latih (MAE)**
```python
from sklearn.metrics import mean_absolute_error
print('MAE:', round(mean_absolute_error(y, model.predict(d)), 2), 'miliar')
```

---

## Bagian D — Model Pertumbuhan (%) via Log

**Sel 13 — regresi log-linear (pertumbuhan persen)**
```python
import numpy as np
d['log_pendapatan'] = np.log(d['pendapatan_miliar'])
m_log = smf.ols('log_pendapatan ~ tahun', data=d).fit()
growth = (np.exp(m_log.params['tahun']) - 1) * 100
print('Pertumbuhan per tahun:', round(growth, 1), '%')
```
▶ Amati: koef pada model log ≈ laju pertumbuhan **persen** (mirip CAGR).

---

## Bagian E — Bandingkan Semua Sektor

**Sel 14 — kenaikan/tahun & pertumbuhan% tiap sektor**
```python
hasil = []
for s in sektor['sektor'].unique():
    sub = sektor[sektor['sektor'] == s].copy()
    m = smf.ols('pendapatan_miliar ~ tahun', data=sub).fit()
    sub['logp'] = np.log(sub['pendapatan_miliar'])
    ml = smf.ols('logp ~ tahun', data=sub).fit()
    hasil.append({'sektor': s,
                  'naik_per_thn': m.params['tahun'],
                  'growth_%': (np.exp(ml.params['tahun']) - 1) * 100,
                  'R2': m.rsquared})
rank = pd.DataFrame(hasil).sort_values('growth_%', ascending=False)
rank.round(2)
```

**Sel 15 — grafik ranking pertumbuhan %**
```python
rank.plot(x='sektor', y='growth_%', kind='barh', legend=False)
plt.title('Pertumbuhan per Tahun (%)'); plt.show()
```

**Sel 16 — simpan**
```python
rank.to_csv('ranking_pertumbuhan_sektor.csv', index=False)
print('Tersimpan: ranking_pertumbuhan_sektor.csv')
```

> ⚠️ Regresi linear mengasumsikan tren LURUS. Jangan ekstrapolasi terlalu jauh;
> pertumbuhan nyata sering melambat. Korelasi ≠ sebab-akibat.

---

## Latihan Mandiri

1. 'Jasa Keuangan': kenaikan/tahun, growth %, R²?
2. Sektor dengan R² terendah — kenapa (lihat trennya)?
3. Proyeksikan 'Manufaktur' ke 2025–2028.
4. Model mana lebih masuk akal untuk 'Teknologi': linear atau log? Argumen.
5. Sektor mana yang **nilai absolut**-nya besar tapi **pertumbuhan %**-nya kecil?
6. Hitung total pendapatan semua sektor per tahun (groupby tahun) & regresikan.

---

## 🏁 Tantangan 45 Menit — "Proyeksi Portofolio Sektor"

1. Untuk tiap sektor, proyeksikan pendapatan 2025–2027 (model linear).
2. Susun jadi satu tabel: baris=sektor, kolom=tahun (2025,2026,2027).
3. Hitung total portofolio per tahun proyeksi.
4. Grafik garis: aktual (2015–2024) + proyeksi (2025–2027) untuk 3 sektor teratas.
5. Simpan tabel proyeksi ke `proyeksi_portofolio.xlsx` + tulis 2 rekomendasi (`#`).

✅ **Selesai bila:** Anda bisa membaca output regresi, memilih model linear vs log,
memproyeksikan, dan membandingkan pertumbuhan antar sektor.

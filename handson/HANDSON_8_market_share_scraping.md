# Hands-On 8 — Market Share + Web & Document Scraping (± 45 menit)

> Satu sel per langkah. Ketik sendiri, Shift+Enter, amati.

**Tujuan:** penetrasi/market share per populasi, web scraping (`read_html` + BS4),
document scraping (pdfplumber), gabung 3 sumber jadi laporan, etika.
**Data:** `data/populasi_provinsi.csv`, `data/sample_populasi.html`, `data/laporan_keuangan.pdf`.
**Buat notebook:** `latihan_h8.ipynb`.
**Library:** `pip install beautifulsoup4 lxml pdfplumber html5lib openpyxl`

---

## Bagian A — Market Share Berbasis Populasi

**Sel 1 — muat data**

```python
import pandas as pd
p = pd.read_csv('data/populasi_provinsi.csv')
p
```

**Sel 2 — hitung penetrasi**

```python
p['penetrasi'] = p['nasabah_kita'] / p['populasi']
p.sort_values('penetrasi')
```

**Sel 3 — market share terhadap total nasabah kita**

```python
p['share_nasabah'] = p['nasabah_kita'] / p['nasabah_kita'].sum()
p[['provinsi', 'share_nasabah']].sort_values('share_nasabah', ascending=False)
```

**Sel 4 — skor peluang (populasi besar, penetrasi rendah)**

```python
p['peluang'] = p['populasi'] * (p['penetrasi'].mean() - p['penetrasi'])
p.sort_values('peluang', ascending=False)[['provinsi', 'populasi', 'penetrasi', 'peluang']].head()
```

**Sel 5 — visualisasi penetrasi**

```python
import matplotlib.pyplot as plt
p.sort_values('penetrasi').plot(x='provinsi', y='penetrasi', kind='barh', legend=False)
plt.title('Penetrasi per Provinsi'); plt.xlabel('nasabah / populasi'); plt.show()
```

---

## Bagian B — Web Scraping

**Sel 6 — cara tercepat: pd.read_html**

```python
tabel = pd.read_html('data/sample_populasi.html')
print('Jumlah tabel:', len(tabel))
web = tabel[0]; web.head()
```

▶ Untuk situs online, ganti path → URL.

**Sel 7 — BeautifulSoup: judul & header**

```python
from bs4 import BeautifulSoup
html = open('data/sample_populasi.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'lxml')
print(soup.find('h1').text)
print([th.text for th in soup.select('table#populasi th')])
```

**Sel 8 — BeautifulSoup: ambil baris tabel**

```python
baris = []
for tr in soup.select('table#populasi tbody tr'):
    baris.append([td.text for td in tr.find_all('td')])
baris[:3]
```

**Sel 9 — rapikan angka populasi (teks → int)**

```python
web['Populasi'] = web['Populasi'].astype(str).str.replace(',', '').astype(int)
web.dtypes
```

**Sel 10 — gabung web dengan data internal**

```python
gab = p.merge(web[['Provinsi', 'Populasi']], left_on='provinsi', right_on='Provinsi', how='left')
gab[['provinsi', 'populasi', 'Populasi']].head()
```

**Sel 11 — sopan santun scraping (jeda antar-request)**

```python
import time
for hal in range(1, 4):
    # r = requests.get(f'{url}?page={hal}', headers={'User-Agent':'workshop'})
    print('Ambil halaman', hal); time.sleep(1)   # beri jeda 1 detik
```

▶ Amati: `time.sleep` mencegah membebani server. Wajib untuk scraping nyata.

> **Untuk situs sungguhan (referensi — jangan tanpa izin):**
>
> ```python
> import requests
> r = requests.get(url, headers={'User-Agent': 'workshop-naradacode'})
> tabel = pd.read_html(r.text)
> ```

---

## Bagian C — Document Scraping (PDF)

**Sel 12 — ekstrak teks**

```python
import pdfplumber
with pdfplumber.open('data/laporan_keuangan.pdf') as pdf:
    teks = pdf.pages[0].extract_text()
print(teks[:300])
```

**Sel 13 — ekstrak tabel → DataFrame**

```python
with pdfplumber.open('data/laporan_keuangan.pdf') as pdf:
    tabel_pdf = pdf.pages[0].extract_table()
pdf_df = pd.DataFrame(tabel_pdf[1:], columns=tabel_pdf[0])
pdf_df
```

**Sel 14 — rapikan tipe angka**

```python
pdf_df['Pendapatan (miliar)'] = pd.to_numeric(pdf_df['Pendapatan (miliar)'])
pdf_df.sort_values('Pendapatan (miliar)', ascending=False)
```

**Sel 15 — kontribusi tiap sektor (%)**

```python
total = pdf_df['Pendapatan (miliar)'].sum()
pdf_df['kontribusi_%'] = (pdf_df['Pendapatan (miliar)'] / total * 100).round(1)
pdf_df.sort_values('kontribusi_%', ascending=False)
```

---

## Bagian D — Gabung 3 Sumber & Simpan Laporan

**Sel 16 — laporan multi-sheet (internal + web + pdf)**

```python
with pd.ExcelWriter('market_intelligence.xlsx') as xl:
    p.to_excel(xl, sheet_name='penetrasi', index=False)
    web.to_excel(xl, sheet_name='populasi_web', index=False)
    pdf_df.to_excel(xl, sheet_name='sektor_pdf', index=False)
print('Tersimpan: market_intelligence.xlsx (3 sheet)')
```

▶ Amati: satu file Excel, tiga sumber — siap dibagikan.

---

## Bagian E — Etika & Legal (DISKUSI wajib)

- **Izin & ToS:** cek Terms of Service & `robots.txt` sebelum scraping.
- **Beban server:** beri jeda (`time.sleep`), jangan bertubi-tubi.
- **Identitas:** `User-Agent` wajar; jangan menyamar berbahaya.
- **Data pribadi:** patuhi **UU PDP** — jangan kumpulkan data pribadi tanpa dasar.
- **Utamakan API resmi** bila ada (lebih stabil & legal).
- **Sitasi sumber & tanggal** ambil data.

---

## Latihan Mandiri

1. Provinsi penetrasi rendah tapi populasi besar (prioritas ekspansi)?
2. Total populasi 10 provinsi dari `web` vs jumlah `p['populasi']` — cocok?
3. Dari `pdf_df`, sektor penyumbang terbesar & persentasenya?
4. Tambahkan kolom `target_nasabah` = populasi × penetrasi rata-rata nasional. Selisih dg aktual?
5. Tulis 3 risiko etis/legal men-scrape situs kompetitor.
6. Simpan `pdf_df` (dengan kontribusi) ke `kontribusi_sektor.csv`.

---

## 🏁 Tantangan 45 Menit — "Market Intelligence Brief"

Gabungkan analitik internal + data eksternal jadi 1 brief:

1. Ranking 3 provinsi prioritas ekspansi (skor peluang) + alasan angka.
2. Verifikasi populasi internal vs sumber web (selisih %).
3. Struktur sektor ekonomi dari PDF (kontribusi %) — sektor mana didanai lebih agresif?
4. Simpan semua tabel ke `market_intelligence.xlsx` (multi-sheet).
5. Tulis ringkasan eksekutif 5 kalimat (sel Markdown) + 3 rekomendasi.

✅ **Selesai bila:** Anda menghitung penetrasi/market share, menarik tabel web & PDF,
menggabung 3 sumber ke satu laporan Excel, dan bisa menyebut batas etis scraping.

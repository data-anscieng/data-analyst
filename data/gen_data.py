"""
gen_data.py — Data sintetis untuk Workshop Python Analisis Data & Riset (naradacode).
Semua data DUMMY (dibangkitkan, bukan data nasabah asli). Seed tetap -> reprodusibel.

Menghasilkan:
  data/nasabah_loan.xlsx        -> explore/EDA (H2,H3,H4,H6) + segmentasi (H8) + risk (H9) + uji hipotesis (H11)
  data/penjualan_sektor.csv     -> reshape (H5) + regresi/projeksi (H7) + skenario/CAGR (H12)
  data/populasi_provinsi.csv    -> market share by populasi (H10)
  data/sample_populasi.html     -> latihan web scraping (H10)
  data/laporan_keuangan.pdf     -> latihan document scraping (H10)

Run:
  uv run --python 3.12 --with pandas --with numpy --with openpyxl --with reportlab gen_data.py
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 2000

# ── 1) Data nasabah / loan ───────────────────────────────────────────────────
wilayah = ["Jabodetabek", "Jawa Barat", "Jawa Tengah", "Jawa Timur",
           "Sumatera", "Kalimantan", "Sulawesi", "Indonesia Timur"]
segmen_pekerjaan = ["Karyawan", "Wiraswasta", "PNS/BUMN", "Profesional"]

usia = rng.integers(21, 60, N)
lama_kerja = np.clip((usia - 20) * rng.uniform(0.2, 0.8, N), 0.5, 35).round(1)
pekerjaan = rng.choice(segmen_pekerjaan, N, p=[0.45, 0.28, 0.17, 0.10])

# pendapatan bulanan (juta rupiah) — bergantung usia, lama kerja, pekerjaan
base_inc = 4 + lama_kerja * 0.35 + (usia - 21) * 0.08
job_mult = np.select(
    [pekerjaan == "Karyawan", pekerjaan == "Wiraswasta",
     pekerjaan == "PNS/BUMN", pekerjaan == "Profesional"],
    [1.0, 1.25, 1.1, 1.6])
pendapatan_juta = np.clip(base_inc * job_mult * rng.lognormal(0, 0.25, N), 3, 120).round(2)

jumlah_pinjaman_juta = np.clip(
    pendapatan_juta * rng.uniform(6, 30, N), 10, 2000).round(0)
tenor_bulan = rng.choice([12, 24, 36, 48, 60], N, p=[0.1, 0.25, 0.3, 0.2, 0.15])

# cicilan bulanan (bunga flat sederhana ~ 12%/thn) & Debt Burden Ratio
bunga = 0.12
cicilan = (jumlah_pinjaman_juta * (1 + bunga * tenor_bulan / 12) / tenor_bulan)
dbr = np.clip(cicilan / pendapatan_juta, 0.05, 0.95).round(3)  # rasio cicilan/pendapatan

jumlah_tanggungan = rng.integers(0, 5, N)

# days past due maksimum (proxy perilaku bayar)
dpd_lambda = 2 + dbr * 30 + (jumlah_tanggungan * 1.5)
dpd_max = np.clip(rng.poisson(dpd_lambda), 0, 180)

# ── target default (0=lancar, 1=gagal bayar) — fungsi risiko + noise ──────────
logit = (-3.2
         + 4.0 * (dbr - 0.35)
         + 0.020 * dpd_max
         + 0.10 * jumlah_tanggungan
         - 0.015 * pendapatan_juta
         + 0.02 * (usia < 25))
prob_default = 1 / (1 + np.exp(-logit))
status_default = (rng.uniform(0, 1, N) < prob_default).astype(int)

nasabah = pd.DataFrame({
    "nasabah_id": [f"N{100000+i}" for i in range(N)],
    "usia": usia,
    "pekerjaan": pekerjaan,
    "wilayah": rng.choice(wilayah, N),
    "lama_kerja_thn": lama_kerja,
    "jumlah_tanggungan": jumlah_tanggungan,
    "pendapatan_juta": pendapatan_juta,
    "jumlah_pinjaman_juta": jumlah_pinjaman_juta,
    "tenor_bulan": tenor_bulan,
    "cicilan_juta": cicilan.round(2),
    "dbr": dbr,                       # Debt Burden Ratio
    "dpd_max": dpd_max,              # max days past due
    "status_default": status_default,
})

# sisipkan beberapa missing value supaya ada latihan cleaning (H3)
miss_idx = rng.choice(N, size=60, replace=False)
nasabah.loc[miss_idx[:30], "pendapatan_juta"] = np.nan
nasabah.loc[miss_idx[30:], "lama_kerja_thn"] = np.nan
# beberapa duplikat baris
nasabah = pd.concat([nasabah, nasabah.iloc[:8]], ignore_index=True)

nasabah.to_excel("nasabah_loan.xlsx", index=False)
print(f"nasabah_loan.xlsx        rows={len(nasabah)} default_rate={status_default.mean():.1%}")

# ── 2) Penjualan per sektor per tahun (untuk regresi/projeksi H5) ─────────────
tahun = np.arange(2015, 2025)
sektor_info = {          # (nilai awal 2015 dlm miliar, pertumbuhan/thn, noise)
    "Pertanian":     (120, 0.04, 6),
    "Manufaktur":    (300, 0.06, 12),
    "Perdagangan":   (250, 0.08, 10),
    "Konstruksi":    (180, 0.07, 9),
    "Jasa Keuangan": (150, 0.11, 8),
    "Teknologi":     (60,  0.22, 7),
}
rows = []
for sektor, (awal, growth, noise) in sektor_info.items():
    for i, th in enumerate(tahun):
        nilai = awal * (1 + growth) ** i + rng.normal(0, noise)
        rows.append({"tahun": int(th), "sektor": sektor,
                     "pendapatan_miliar": round(float(max(nilai, 1)), 1)})
sektor = pd.DataFrame(rows)
sektor.to_csv("penjualan_sektor.csv", index=False)
print(f"penjualan_sektor.csv     rows={len(sektor)}")

# ── 3) Populasi & nasabah per provinsi (market share H8) ──────────────────────
prov = pd.DataFrame({
    "provinsi": ["DKI Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur",
                 "Banten", "Sumatera Utara", "Sulawesi Selatan", "Bali",
                 "Kalimantan Timur", "Yogyakarta"],
    "populasi": [10_560_000, 48_270_000, 36_520_000, 40_670_000,
                 11_900_000, 15_180_000, 9_070_000, 4_320_000,
                 3_770_000, 3_670_000],
})
# nasabah bank kita (dummy) — penetrasi berbeda tiap provinsi
penetrasi = rng.uniform(0.03, 0.11, len(prov))
prov["nasabah_kita"] = (prov["populasi"] * penetrasi).astype(int)
prov.to_csv("populasi_provinsi.csv", index=False)
print(f"populasi_provinsi.csv    rows={len(prov)}")

# ── 4) HTML tabel populasi (latihan web scraping H8) ──────────────────────────
html = """<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">
<title>Statistik Populasi Provinsi (Contoh)</title></head>
<body>
<h1>Data Populasi Provinsi — Contoh Latihan Scraping</h1>
<p>Sumber: DUMMY untuk workshop naradacode. Bukan angka resmi.</p>
<table id="populasi" border="1">
<thead><tr><th>Provinsi</th><th>Populasi</th><th>Ibu Kota</th></tr></thead>
<tbody>
""" + "\n".join(
    f"<tr><td>{r.provinsi}</td><td>{r.populasi:,}</td><td>-</td></tr>"
    for r in prov.itertuples()
) + """
</tbody></table>
</body></html>"""
with open("sample_populasi.html", "w", encoding="utf-8") as f:
    f.write(html)
print("sample_populasi.html     ok")

# ── 5) PDF laporan keuangan (latihan document scraping H8) ────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet

    doc = SimpleDocTemplate("laporan_keuangan.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    story = [
        Paragraph("Laporan Ringkas Kinerja Sektor (Contoh)", styles["Title"]),
        Paragraph("Dokumen DUMMY untuk latihan document scraping — naradacode.",
                  styles["Normal"]),
        Spacer(1, 16),
        Paragraph("Tabel 1. Pendapatan per Sektor 2024 (miliar Rupiah)",
                  styles["Heading2"]),
    ]
    tbl = sektor[sektor.tahun == 2024][["sektor", "pendapatan_miliar"]]
    data = [["Sektor", "Pendapatan (miliar)"]] + tbl.values.tolist()
    t = Table(data, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16A34A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))
    story += [t, Spacer(1, 16),
              Paragraph("Catatan: Teknologi tumbuh paling cepat (~22%/tahun); "
                        "Jasa Keuangan menyusul (~11%/tahun).", styles["Normal"])]
    doc.build(story)
    print("laporan_keuangan.pdf     ok")
except Exception as e:
    print(f"laporan_keuangan.pdf     SKIP ({e}) — install reportlab untuk PDF")

print("SELESAI. Semua data dummy tersimpan di folder data/.")

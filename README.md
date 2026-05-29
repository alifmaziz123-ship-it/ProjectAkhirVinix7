# Analisis Sentimen D'Las Lembah Asri 🌿

Dashboard interaktif analisis sentimen ulasan wisata **D'Las Lembah Asri Serang, Purbalingga** dari Google Maps menggunakan metode **Complement Naive Bayes + TF-IDF + Class Weight Balancing**.

---

## 📋 Fitur Dashboard

- **Distribusi Sentimen** — Donut chart & bar bintang 1–5
- **Tren Tahunan 2016–2024** — Stacked bar label asli vs prediksi model berbobot
- **Perbandingan Model** — Confusion matrix, precision/recall/F1 sebelum dan sesudah bobot
- **Radar Chart** — Visualisasi peningkatan recall per kelas
- **Class Weight Balancing** — Penjelasan kenapa bobot diperlukan & efeknya
- **Penyebab Rating Rendah** — Analisis tema keluhan ulasan bintang 1–2
- **Top Keywords** — Kata kunci dominan per sentimen
- **Contoh Ulasan** — Sample review clickable per kategori
- **Metodologi** — Pipeline & parameter lengkap

---

## 🚀 Cara Menjalankan Lokal

```bash
# 1. Clone / ekstrak project
cd dlas-sentiment

# 2. Install dependencies
npm install

# 3. Jalankan development server
npm start
# → buka http://localhost:3000
```

---

## ☁️ Deploy ke Vercel (Gratis, Rekomendasi)

### Cara 1 — Via Vercel CLI
```bash
npm install -g vercel
vercel login
vercel --prod
```

### Cara 2 — Via GitHub + Vercel Dashboard
1. Push project ke GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/USERNAME/dlas-sentiment.git
   git push -u origin main
   ```
2. Buka [vercel.com](https://vercel.com) → **Add New Project**
3. Import repo GitHub → **Deploy**
4. Selesai! URL otomatis tersedia.

---

## ☁️ Deploy ke Netlify (Alternatif)

### Cara 1 — Drag & Drop Build Folder
```bash
npm run build
```
Lalu drag folder `build/` ke [app.netlify.com/drop](https://app.netlify.com/drop)

### Cara 2 — Via GitHub + Netlify Dashboard
1. Push ke GitHub (sama seperti di atas)
2. Buka [netlify.com](https://netlify.com) → **Add new site** → **Import from Git**
3. Build command: `npm run build` | Publish dir: `build`
4. **Deploy site**

---

## 📁 Struktur Project

```
dlas-sentiment/
├── public/
│   └── index.html
├── src/
│   ├── App.jsx          ← Komponen utama (semua chart & UI)
│   ├── data.js          ← Data hasil analisis Python/sklearn
│   ├── App.css
│   └── index.js
├── package.json
├── vercel.json          ← Konfigurasi Vercel
├── netlify.toml         ← Konfigurasi Netlify
├── .gitignore
└── README.md
```

---

## 🛠️ Stack Teknologi

| Komponen | Library |
|---|---|
| UI Framework | React 18 |
| Charts | Recharts 2.x |
| Icons | Lucide React |
| Styling | Inline CSS (no framework) |
| ML (preprocessing) | scikit-learn (Python) |
| Data extraction | pandas, numpy |

---

## 📊 Hasil Model

| Metrik | Tanpa Bobot | Dengan Bobot |
|---|---|---|
| Akurasi | 85,9% | 81,5% |
| Macro F1 | 0,6496 | **0,6612 ↑** |
| Recall Negatif | 52,9% | **82,4% ↑** |
| Recall Netral | 53,5% | **75,6% ↑** |

> **Kesimpulan:** Pembobotan menurunkan akurasi keseluruhan sedikit, tetapi Macro F1 naik dan recall untuk kelas minoritas meningkat drastis — ini yang diinginkan pada data imbalanced.

---

## 👨‍💻 Tentang Data

- **Sumber:** Google Maps Reviews — D'Las Lembah Asri Serang Purbalingga
- **Total:** 5.296 ulasan (setelah filter & preprocessing)
- **Periode:** 2016 – 2024
- **Labeling:** ⭐1–2 = Negatif | ⭐3 = Netral | ⭐4–5 = Positif

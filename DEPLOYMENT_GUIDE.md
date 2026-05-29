# 📊 D'Las Sentiment Analysis - Streamlit Deployment

Panduan lengkap deploy aplikasi Streamlit ke web.

## 🚀 Quick Start (Local Testing)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Locally
```bash
streamlit run app.py
```
Aplikasi akan terbuka di: `http://localhost:8501`

---

## 🌐 Deploy ke Streamlit Cloud (GRATIS)

### Langkah 1: Push Code ke GitHub
```bash
git init
git add .
git commit -m "Initial Streamlit app commit"
git remote add origin https://github.com/USERNAME/REPONAME.git
git branch -M main
git push -u origin main
```

### Langkah 2: Kunjungi Streamlit Cloud
1. Buka: https://streamlit.io/cloud
2. Klik **"Sign Up"** (atau login jika sudah punya akun)
3. Pilih sign up dengan **GitHub**

### Langkah 3: Deploy App
1. Di dashboard Streamlit Cloud, klik **"New App"**
2. Pilih:
   - **Repository:** USERNAME/REPONAME
   - **Branch:** main
   - **Main file path:** app.py
3. Klik **"Deploy"**

✅ Done! App akan live dalam 1-2 menit.

---

## 📝 File Structure
```
ProjectAkhirVinix7/
├── app.py                 # Main Streamlit app
├── data.py               # Data (hardcoded)
├── requirements.txt      # Dependencies
├── .streamlit/
│   └── config.toml      # Streamlit config
└── README.md            # This file
```

---

## ⚙️ Alternative: Deploy ke Heroku/Railway/Render

### Option 1: Railway (Recommended - Easiest)
1. Buka: https://railway.app
2. Sign up dengan GitHub
3. Klik **"New Project"** → **"Deploy from GitHub Repo"**
4. Select repository → Railway akan auto-detect `requirements.txt`
5. Tunggu deploy selesai

### Option 2: Render
1. Buka: https://render.com
2. Buat file `render.yaml`:
```yaml
services:
  - type: web
    name: dlas-sentiment
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run app.py
    envVars:
      - key: PORT
        value: 8501
```
3. Push ke GitHub dan connect di Render

---

## 📦 Features
- ✅ Dashboard Overview (Sentiment Distribution, Star Ratings)
- ✅ Model Performance (Confusion Matrix, Metrics)
- ✅ Yearly & Monthly Trends
- ✅ Word Analysis & Themes
- ✅ Sample Reviews

---

## 🔧 Troubleshooting

### Error: Module not found
```bash
pip install streamlit pandas plotly
```

### App loading slowly
Streamlit Cloud gratis punya resource terbatas. Untuk production, gunakan paid tier atau Railway/Render.

### Data tidak tampil
Pastikan `data.py` ada di folder yang sama dengan `app.py`

---

## 📚 Resources
- Streamlit Docs: https://docs.streamlit.io
- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-cloud/get-started
- Plotly Docs: https://plotly.com/python/

---

## 💡 Tips
- **Update data**: Edit `data.py` dan push ke GitHub, Streamlit Cloud akan auto-redeploy
- **Custom domain**: Upgrade ke Streamlit Community Cloud paid tier
- **Performance**: Gunakan `@st.cache_data` untuk caching hasil komputasi berat

Selamat deploy! 🎉

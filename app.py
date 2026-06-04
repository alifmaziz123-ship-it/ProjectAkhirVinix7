import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data_loader import DATA
import json
import os
import base64
from datetime import datetime

# Sentiment label mapping (internal keys -> display labels in Indonesian)
SENTIMENT_LABELS = {'Positif': 'Positif', 'Netral': 'Netral', 'Negatif': 'Negatif'}
INV_SENTIMENT = {v: k for k, v in SENTIMENT_LABELS.items()}

# Page config
st.set_page_config(
    page_title="D'Las Sentiment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for new reviews
if 'new_reviews' not in st.session_state:
    try:
        with open('new_reviews.json', 'r', encoding='utf-8') as f:
            st.session_state.new_reviews = json.load(f)
    except:
        st.session_state.new_reviews = {'Positif': [], 'Netral': [], 'Negatif': []}

def save_reviews():
    """Save reviews to JSON file"""
    with open('new_reviews.json', 'w', encoding='utf-8') as f:
        json.dump(st.session_state.new_reviews, f, ensure_ascii=False, indent=2)


def get_data_uri_for_image(path: str) -> str | None:
    """Return a data URI for the given local image path, or None if not found/failed."""
    try:
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = f.read()
            ext = os.path.splitext(path)[1].lower().lstrip('.')
            mime = 'image/jpeg' if ext in ['jpg', 'jpeg'] else f'image/{ext}'
            return f"data:{mime};base64,{base64.b64encode(data).decode()}"
    except Exception:
        return None
    return None

# Custom CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(180deg, #eef6ff 0%, #f8fbff 40%, #ffffff 100%);
        color-scheme: light;
    }
    .stApp {
        background: transparent;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    .stApp .main {
        background: transparent;
    }
    .hero-block {
        background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.12), transparent 35%),
                    linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        /* Subtle Mount Slamet SVG silhouette embedded as a data URI */
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 400'><path d='M0 300 L150 100 L300 300 L450 150 L600 300 L800 80 L800 400 L0 400 Z' fill='%23304f2b' opacity='0.12'/><path d='M0 320 L160 140 L320 320 L480 180 L640 320 L800 120 L800 400 L0 400 Z' fill='%233a6b3d' opacity='0.09'/></svg>");
        background-repeat: no-repeat;
        background-position: left bottom;
        background-size: 48% auto;
        border: 1px solid rgba(96, 165, 250, 0.22);
        border-radius: 28px;
        padding: 32px;
        box-shadow: 0 28px 90px rgba(15, 23, 42, 0.08);
        margin-bottom: 24px;
    }
    .app-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.4rem;
    }
    .app-subtitle {
        font-size: 1.05rem;
        color: #334155;
        line-height: 1.75;
        max-width: 820px;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 20px;
        padding: 24px;
        min-height: 120px;
    }
    .metric-card .label {
        color: #475569;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    .metric-card .value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    .metric-card .caption {
        color: #64748b;
        font-size: 0.92rem;
    }
    .streamlit-expanderHeader {
        font-weight: 700;
    }
    .sidebar .css-6qob1r {
        padding-top: 1rem;
    }
    .css-1d391kg .block-container {
        padding-top: 0px;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stSidebar {
        background: rgba(255,255,255,0.96) !important;
        border: 1px solid rgba(96, 165, 250, 0.18);
        box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
    }
    .css-1v3fvcr {
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Sentiment Analysis Dashboard")
st.sidebar.markdown(f"**Data Source:** {DATA['meta']['source']}")
st.sidebar.markdown(f"**Total Data:** {DATA['meta']['total_data']:,}")
st.sidebar.markdown(f"**Period:** {DATA['meta']['period']}")
# Provide filtered CSV download if available
if os.path.exists('datagabung_5y.csv'):
    with open('datagabung_5y.csv', 'rb') as f:
        csv_bytes = f.read()
    st.sidebar.download_button(
        label='📥 Download filtered 5-year CSV',
        data=csv_bytes,
        file_name='datagabung_5y.csv',
        mime='text/csv',
        use_container_width=True
    )

# Main content
# Prefer a local hero image if the user adds one to the repo (assets/hero_slamet.jpg,
# static/hero_slamet.jpg, or public/hero_slamet.jpg). Otherwise fall back to Unsplash.
local_candidates = ['assets/hero_slamet.jpg', 'static/hero_slamet.jpg', 'public/hero_slamet.jpg']
hero_img = None
for p in local_candidates:
    hero_img = get_data_uri_for_image(p)
    if hero_img:
        break
if not hero_img:
    hero_img = 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80'

st.markdown(
    f"""
    <div class='hero-block'>
        <div style='display:flex; align-items:center; gap:18px;'>
            <img src="{hero_img}" style='width:280px; height:160px; object-fit:cover; border-radius:12px; box-shadow:0 8px 24px rgba(15,23,42,0.12)' />
            <div>
                <div class='app-title'>🏔️ D'Las Lembah Asri Serang Purbalingga</div>
                <div class='app-subtitle'>Dashboard sentimen ulasan Google Reviews untuk 5 tahun terakhir. Jelajahi tren sentimen, performa model, dan pola ulasan dalam satu tampilan yang bersih dan profesional.</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

positive_pct = (DATA['distribution']['sentiment'].get('Positif', 0) / DATA['meta']['total_data'] * 100) if DATA['meta']['total_data'] else 0.0
latest_year = DATA['yearly']['years'][-1] if DATA['yearly']['years'] else 'N/A'
avg_rating_latest = DATA['yearly']['avg_rating'][-1] if DATA['yearly']['avg_rating'] else 0.0
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Ulasan", f"{DATA['meta']['total_data']:,}")
col2.metric("Persentase Positif", f"{positive_pct:.1f}%")
col3.metric("Tahun Terakhir", latest_year)
col4.metric("Rata-rata Rating", f"{avg_rating_latest:.2f}")

# Tab navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Ringkasan", "📊 Performa Model", "📅 Tren", "💬 Analisis Kata", "📝 Contoh Ulasan", "➕ Tambah Ulasan"])

# ═══════════════════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Distribusi Sentimen")
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment pie chart
        sentiment_data = DATA['distribution']['sentiment']
        # tampilkan label dalam Bahasa Indonesia
        labels_display = [SENTIMENT_LABELS.get(k, k) for k in sentiment_data.keys()]
        values = [v for v in sentiment_data.values()]
        fig_sentiment = go.Figure(data=[go.Pie(
            labels=labels_display,
            values=values,
            marker=dict(colors=['#2a7f4f', '#d97706', '#8b5e3c']),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
        )])
        fig_sentiment.update_layout(
            title="Distribusi Sentimen",
            height=400,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with col2:
        # Star rating distribution
        star_data = DATA['distribution']['stars']
        fig_stars = go.Figure(data=[go.Bar(
            x=list(star_data.keys()),
            y=list(star_data.values()),
            marker_color=['#dc2626', '#ef4444', '#f97316', '#eab308', '#16a34a'],
            hovertemplate='<b>★ %{x}</b><br>Count: %{y}<extra></extra>'
        )])
        fig_stars.update_layout(
            title="Distribusi Rating Bintang",
            xaxis_title="Rating",
            yaxis_title="Jumlah",
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=False
        )
        st.plotly_chart(fig_stars, use_container_width=True)
    
    # KPI Cards
    st.subheader("Metrik Utama")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reviews", f"{DATA['meta']['total_data']:,}")
    with col2:
        st.metric("Training Data", f"{DATA['meta']['train_size']:,}")
    with col3:
        st.metric("Test Data", f"{DATA['meta']['test_size']:,}")
    with col4:
        st.metric("Positive %", f"{(DATA['distribution']['sentiment'].get('Positif',0) / DATA['meta']['total_data'] * 100):.1f}%")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 2: MODEL PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════
with tab2:
    model_choice = st.radio("Pilih Model", ["Tanpa Bobot Kelas", "Dengan Bobot Kelas"], horizontal=True)
    
    if model_choice == "Without Class Weight":
        model = DATA['model_no_weight']
    else:
        model = DATA['model_weighted']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Akurasi", f"{model['accuracy']:.4f}")
    with col2:
        st.metric("Macro F1", f"{model['macro_f1']:.4f}")
    with col3:
        if 'weights' in model:
            st.markdown("**Class Weights:**")
            for cls, weight in model['weights'].items():
                st.write(f"• {cls}: {weight:.4f}")
    
    # Confusion Matrix
    st.subheader("Matriks Kebingungan")
    cm = model['confusion_matrix']
    classes = ['Negatif', 'Netral', 'Positif']
    classes_display = [SENTIMENT_LABELS[c] for c in classes]

    fig_cm = go.Figure(data=go.Heatmap(
        z=cm,
        x=classes_display,
        y=classes_display,
        colorscale='Blues',
        text=cm,
        texttemplate='%{text}',
        textfont={"size": 12},
        hovertemplate='Actual: %{y}<br>Predicted: %{x}<br>Count: %{text}<extra></extra>'
    ))
    fig_cm.update_layout(
        title="Matriks Kebingungan",
        xaxis_title="Prediksi",
        yaxis_title="Sebenarnya",
        height=400
    )
    st.plotly_chart(fig_cm, use_container_width=True)
    
    # Per-class metrics
    st.subheader("Metrik Per-Kelas")
    metrics_data = []
    for class_name, metrics in model['per_class'].items():
        metrics_data.append({
            'Class': SENTIMENT_LABELS.get(class_name, class_name),
            'Precision': metrics['precision'],
            'Recall': metrics['recall'],
            'F1 Score': metrics['f1']
        })
    
    df_metrics = pd.DataFrame(metrics_data)
    st.dataframe(df_metrics, use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 3: TRENDS
# ═══════════════════════════════════════════════════════════════════════════
with tab3:
    col1, col2 = st.columns(2)
    
    # Yearly trends
    with col1:
        st.subheader("Tren Tahunan (2016-2024)")
        yearly = DATA['yearly']
        
        fig_yearly = go.Figure()
        
        fig_yearly.add_trace(go.Scatter(
            x=yearly['years'], y=yearly['sentiment_orig']['Positif'],
            name=SENTIMENT_LABELS['Positif'], line=dict(color='#16a34a', width=3)
        ))
        fig_yearly.add_trace(go.Scatter(
            x=yearly['years'], y=yearly['sentiment_orig']['Netral'],
            name=SENTIMENT_LABELS['Netral'], line=dict(color='#d97706', width=3)
        ))
        fig_yearly.add_trace(go.Scatter(
            x=yearly['years'], y=yearly['sentiment_orig']['Negatif'],
            name=SENTIMENT_LABELS['Negatif'], line=dict(color='#dc2626', width=3)
        ))
        
        fig_yearly.update_layout(
            title="Sentiment by Year",
            xaxis_title="Year",
            yaxis_title="Count",
            height=400,
            hovermode='x unified'
        )
        st.plotly_chart(fig_yearly, use_container_width=True)
    
    # Average rating trend
    with col2:
        st.subheader("Rata-rata Rating per Tahun")
        fig_rating = go.Figure(data=[go.Scatter(
            x=yearly['years'],
            y=yearly['avg_rating'],
            mode='lines+markers',
            line=dict(color='#0C3D2E', width=3),
            marker=dict(size=8),
            fill='tozeroy'
        )])
        fig_rating.update_layout(
            title="Average Rating Trend",
            xaxis_title="Year",
            yaxis_title="Average Rating",
            height=400,
            hovermode='x'
        )
        st.plotly_chart(fig_rating, use_container_width=True)
    
    # Monthly 2024 trends
    st.subheader("Distribusi Bulanan (2024)")
    monthly = DATA['monthly_2024']
    
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Bar(
        x=monthly['month_names'], y=monthly['Positif'],
        name=SENTIMENT_LABELS['Positif'], marker_color='#16a34a'
    ))
    fig_monthly.add_trace(go.Bar(
        x=monthly['month_names'], y=monthly['Netral'],
        name=SENTIMENT_LABELS['Netral'], marker_color='#d97706'
    ))
    fig_monthly.add_trace(go.Bar(
        x=monthly['month_names'], y=monthly['Negatif'],
        name=SENTIMENT_LABELS['Negatif'], marker_color='#dc2626'
    ))
    
    fig_monthly.update_layout(
        barmode='stack',
        title="Distribusi Sentimen Bulanan 2024",
        xaxis_title="Bulan",
        yaxis_title="Jumlah",
        height=400,
        hovermode='x'
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 4: WORD ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
with tab4:
    # Sentiment selector (display English labels)
    sentiment_keys = ['Positif', 'Netral', 'Negatif']
    sentiment_options = [SENTIMENT_LABELS[k] for k in sentiment_keys]
    sentiment_display = st.radio("Pilih Sentimen", sentiment_options, horizontal=True)
    sentiment_filter = INV_SENTIMENT[sentiment_display]

    words = DATA['top_words'][sentiment_filter]
    word_df = pd.DataFrame(words)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Kata Teratas - {SENTIMENT_LABELS[sentiment_filter]}")
        fig_words = go.Figure(data=[go.Bar(
            x=word_df['count'],
            y=word_df['word'],
            orientation='h',
            marker_color={
                'Positif': '#16a34a',
                'Negatif': '#dc2626',
                'Netral': '#d97706'
            }[sentiment_filter],
            text=word_df['count'],
            textposition='outside'
        )])
        fig_words.update_layout(
            title=f"Frekuensi Kata - {SENTIMENT_LABELS.get(sentiment_filter, sentiment_filter)}",
            xaxis_title="Frekuensi",
            yaxis_title="Kata",
            height=500,
            margin=dict(l=100)
        )
        st.plotly_chart(fig_words, use_container_width=True)
    
    with col2:
        st.subheader(f"Tema Negatif")
        neg_themes = DATA['neg_themes']
        
        theme_df = pd.DataFrame([
            {'theme': k, 'count': v} for k, v in neg_themes.items()
        ]).sort_values('count', ascending=True)
        
        fig_themes = go.Figure(data=[go.Bar(
            x=theme_df['count'],
            y=theme_df['theme'],
            orientation='h',
            marker_color='#dc2626',
            text=theme_df['count'],
            textposition='outside'
        )])
        fig_themes.update_layout(
            title="Tema Negatif",
            xaxis_title="Frekuensi",
            yaxis_title="Tema",
            height=500,
            margin=dict(l=180)
        )
        st.plotly_chart(fig_themes, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 5: SAMPLE REVIEWS
# ═══════════════════════════════════════════════════════════════════════════
with tab5:
    sentiment_keys = ['Positif', 'Netral', 'Negatif']
    sentiment_options = [SENTIMENT_LABELS[k] for k in sentiment_keys]
    sentiment_display = st.radio("Pilih Jenis Sentimen", sentiment_options, horizontal=True)
    sentiment_type = INV_SENTIMENT[sentiment_display]

    samples = DATA['samples'][sentiment_type]
    
    color_map = {
        'Positif': '🟢',
        'Negatif': '🔴',
        'Netral': '🟡'
    }
    
    st.subheader(f"{color_map[sentiment_type]} Contoh Ulasan - {SENTIMENT_LABELS.get(sentiment_type, sentiment_type)}")
    
    for idx, sample in enumerate(samples, 1):
        with st.container():
            col1, col2 = st.columns([1, 5])
            
            with col1:
                st.metric("★", sample['stars'])
            
            with col2:
                st.markdown(f"**Date:** {sample['date']}")
                st.markdown(f"> {sample['text']}")
            
            st.divider()

# ═══════════════════════════════════════════════════════════════════════════
# TAB 6: ADD REVIEW
# ═══════════════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("✍️ Tambah Ulasan Baru")
    
    col1, col2 = st.columns(2)
    
    with col1:
        review_stars = st.slider("Rating (bintang)", 1, 5, 5, help="Pilih 1-5 bintang")
        # sentiment select (display English, store internal key)
        review_sentiment_display = st.selectbox(
            "Pilih sentimen",
            [SENTIMENT_LABELS[k] for k in ['Positif','Netral','Negatif']],
            help="Pilih sentimen untuk ulasan Anda"
        )
        review_sentiment = INV_SENTIMENT[review_sentiment_display]
    
    with col2:
        review_date = st.date_input("Tanggal ulasan", datetime.now())
    
    review_text = st.text_area(
        "Tulis ulasan Anda",
        placeholder="Contoh: Tempatnya bagus untuk liburan keluarga, bersih, dan terjangkau...",
        height=150
    )
    
    if st.button("📤 Kirim Ulasan", type="primary", use_container_width=True):
        if review_text.strip() == "":
            st.error("❌ Ulasan tidak boleh kosong!")
        else:
            new_review = {
                "stars": int(review_stars),
                "date": review_date.strftime("%Y-%m-%d"),
                "text": review_text.strip()
            }
            
            # Tambah ke session state
            st.session_state.new_reviews[review_sentiment].append(new_review)
            save_reviews()
            
            st.success("✅ Ulasan berhasil ditambahkan!")
            st.balloons()
    
    st.divider()
    
    # Display new reviews
    st.subheader("📋 Ulasan Baru")
    
    total_new = sum(len(reviews) for reviews in st.session_state.new_reviews.values())
    
    if total_new == 0:
        st.info("No new reviews yet. Add one above! 👆")
    else:
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Ulasan Baru", total_new)
        with col2:
            st.metric(SENTIMENT_LABELS['Positif'], len(st.session_state.new_reviews['Positif']))
        with col3:
            st.metric(SENTIMENT_LABELS['Netral'], len(st.session_state.new_reviews['Netral']))
        with col4:
            st.metric(SENTIMENT_LABELS['Negatif'], len(st.session_state.new_reviews['Negatif']))
        
        st.markdown("---")
        
        # Display all new reviews
        for sentiment in ["Positif", "Netral", "Negatif"]:
            reviews = st.session_state.new_reviews[sentiment]
            if reviews:
                color_map = {
                    'Positif': '🟢',
                    'Negatif': '🔴',
                    'Netral': '🟡'
                }
                
                st.subheader(f"{color_map[sentiment]} {SENTIMENT_LABELS[sentiment]} ({len(reviews)})")
                
                for idx, review in enumerate(reviews, 1):
                    with st.container():
                        col_star, col_content = st.columns([0.5, 5])
                        
                        with col_star:
                            st.metric("★", review['stars'])
                        
                        with col_content:
                            st.caption(f"📅 {review['date']}")
                            st.markdown(f"> {review['text']}")
                        
                        st.divider()
        
        # Download reviews as CSV
        st.subheader("📥 Ekspor Data")
        
        all_new_reviews = []
        for sentiment, reviews in st.session_state.new_reviews.items():
            for review in reviews:
                all_new_reviews.append({
                    'Sentiment': SENTIMENT_LABELS[sentiment],
                    'Rating': review['stars'],
                    'Date': review['date'],
                    'Review': review['text']
                })
        
        if all_new_reviews:
            df_export = pd.DataFrame(all_new_reviews)
            csv = df_export.to_csv(index=False, encoding='utf-8-sig')
            
            st.download_button(
                label="📥 Unduh CSV",
                data=csv,
                file_name=f"ulasan_baru_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Reset data button
            if st.button("🗑️ Hapus Semua Ulasan Baru", type="secondary", use_container_width=True):
                st.session_state.new_reviews = {'Positif': [], 'Netral': [], 'Negatif': []}
                save_reviews()
                st.rerun()

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #475569; font-size: 13px;'>
    <p>Dashboard Analisis Sentimen D'Las Lembah Asri Serang Purbalingga</p>
    <p>Sumber Data: Google Maps Reviews | Periode: {DATA['meta']['period']}</p>
    <p style='font-size:11px; color:#94a3b8'>Dibuat otomatis — data difilter 5 tahun terakhir</p>
</div>
""", unsafe_allow_html=True)

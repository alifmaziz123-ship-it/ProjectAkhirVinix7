import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from data import DATA
import json
from datetime import datetime

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

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
    }
    .positive { color: #16a34a; }
    .neutral { color: #d97706; }
    .negative { color: #dc2626; }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Sentiment Analysis Dashboard")
st.sidebar.markdown(f"**Data Source:** {DATA['meta']['source']}")
st.sidebar.markdown(f"**Total Data:** {DATA['meta']['total_data']:,}")
st.sidebar.markdown(f"**Period:** {DATA['meta']['period']}")

# Main content
st.title("🏔️ D'Las Lembah Asri - Analisis Sentimen Google Reviews")
st.markdown(f"*{DATA['meta']['title']}*")

# Tab navigation
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Overview", "📊 Model Performance", "📅 Trends", "💬 Word Analysis", "📝 Sample Reviews", "➕ Add Review"])

# ═══════════════════════════════════════════════════════════════════════════
# TAB 1: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Sentiment Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        # Sentiment pie chart
        sentiment_data = DATA['distribution']['sentiment']
        fig_sentiment = go.Figure(data=[go.Pie(
            labels=list(sentiment_data.keys()),
            values=list(sentiment_data.values()),
            marker=dict(colors=['#16a34a', '#d97706', '#dc2626']),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>'
        )])
        fig_sentiment.update_layout(
            title="Sentiment Distribution",
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
            title="Star Rating Distribution",
            xaxis_title="Rating",
            yaxis_title="Count",
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=False
        )
        st.plotly_chart(fig_stars, use_container_width=True)
    
    # KPI Cards
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reviews", f"{DATA['meta']['total_data']:,}")
    with col2:
        st.metric("Training Data", f"{DATA['meta']['train_size']:,}")
    with col3:
        st.metric("Test Data", f"{DATA['meta']['test_size']:,}")
    with col4:
        st.metric("Positive %", f"{(DATA['distribution']['sentiment']['Positif'] / DATA['meta']['total_data'] * 100):.1f}%")

# ═══════════════════════════════════════════════════════════════════════════
# TAB 2: MODEL PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════
with tab2:
    model_choice = st.radio("Select Model", ["Without Class Weight", "With Class Weight"], horizontal=True)
    
    if model_choice == "Without Class Weight":
        model = DATA['model_no_weight']
    else:
        model = DATA['model_weighted']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accuracy", f"{model['accuracy']:.4f}")
    with col2:
        st.metric("Macro F1 Score", f"{model['macro_f1']:.4f}")
    with col3:
        if 'weights' in model:
            st.markdown("**Class Weights:**")
            for cls, weight in model['weights'].items():
                st.write(f"• {cls}: {weight:.4f}")
    
    # Confusion Matrix
    st.subheader("Confusion Matrix")
    cm = model['confusion_matrix']
    classes = ['Negatif', 'Netral', 'Positif']
    
    fig_cm = go.Figure(data=go.Heatmap(
        z=cm,
        x=classes,
        y=classes,
        colorscale='Blues',
        text=cm,
        texttemplate='%{text}',
        textfont={"size": 12},
        hovertemplate='Actual: %{y}<br>Predicted: %{x}<br>Count: %{text}<extra></extra>'
    ))
    fig_cm.update_layout(
        title="Confusion Matrix",
        xaxis_title="Predicted",
        yaxis_title="Actual",
        height=400
    )
    st.plotly_chart(fig_cm, use_container_width=True)
    
    # Per-class metrics
    st.subheader("Per-Class Performance Metrics")
    metrics_data = []
    for class_name, metrics in model['per_class'].items():
        metrics_data.append({
            'Class': class_name,
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
        st.subheader("Yearly Trends (2016-2024)")
        yearly = DATA['yearly']
        
        fig_yearly = go.Figure()
        
        fig_yearly.add_trace(go.Scatter(
            x=yearly['years'], y=yearly['sentiment_orig']['Positif'],
            name='Positif', line=dict(color='#16a34a', width=3)
        ))
        fig_yearly.add_trace(go.Scatter(
            x=yearly['years'], y=yearly['sentiment_orig']['Netral'],
            name='Netral', line=dict(color='#d97706', width=3)
        ))
        fig_yearly.add_trace(go.Scatter(
            x=yearly['years'], y=yearly['sentiment_orig']['Negatif'],
            name='Negatif', line=dict(color='#dc2626', width=3)
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
        st.subheader("Average Rating by Year")
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
    st.subheader("Monthly Distribution (2024)")
    monthly = DATA['monthly_2024']
    
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Bar(
        x=monthly['month_names'], y=monthly['Positif'],
        name='Positif', marker_color='#16a34a'
    ))
    fig_monthly.add_trace(go.Bar(
        x=monthly['month_names'], y=monthly['Netral'],
        name='Netral', marker_color='#d97706'
    ))
    fig_monthly.add_trace(go.Bar(
        x=monthly['month_names'], y=monthly['Negatif'],
        name='Negatif', marker_color='#dc2626'
    ))
    
    fig_monthly.update_layout(
        barmode='stack',
        title="Monthly Sentiment Distribution 2024",
        xaxis_title="Month",
        yaxis_title="Count",
        height=400,
        hovermode='x'
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 4: WORD ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
with tab4:
    sentiment_filter = st.radio("Select Sentiment", ["Positif", "Negatif", "Netral"], horizontal=True)
    
    words = DATA['top_words'][sentiment_filter]
    word_df = pd.DataFrame(words)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Top Words - {sentiment_filter}")
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
            title=f"Word Frequency - {sentiment_filter}",
            xaxis_title="Frequency",
            yaxis_title="Word",
            height=500,
            margin=dict(l=100)
        )
        st.plotly_chart(fig_words, use_container_width=True)
    
    with col2:
        st.subheader(f"Negative Themes")
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
            title="Negative Themes",
            xaxis_title="Frequency",
            yaxis_title="Theme",
            height=500,
            margin=dict(l=180)
        )
        st.plotly_chart(fig_themes, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════
# TAB 5: SAMPLE REVIEWS
# ═══════════════════════════════════════════════════════════════════════════
with tab5:
    sentiment_type = st.radio("Select Sentiment Type", ["Positif", "Negatif", "Netral"], horizontal=True)
    
    samples = DATA['samples'][sentiment_type]
    
    color_map = {
        'Positif': '🟢',
        'Negatif': '🔴',
        'Netral': '🟡'
    }
    
    st.subheader(f"{color_map[sentiment_type]} Sample Reviews - {sentiment_type}")
    
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
        review_stars = st.slider("Berapa rating bintang?", 1, 5, 5, help="Pilih 1-5 bintang")
        review_sentiment = st.selectbox(
            "Pilih sentimen",
            ["Positif", "Netral", "Negatif"],
            help="Pilih sentimen berdasarkan review Anda"
        )
    
    with col2:
        review_date = st.date_input("Tanggal review", datetime.now())
    
    review_text = st.text_area(
        "Tulis ulasan Anda",
        placeholder="Contoh: Tempatnya sangat bagus dan cocok untuk liburan keluarga...",
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
            
            # Add to session state
            st.session_state.new_reviews[review_sentiment].append(new_review)
            save_reviews()
            
            st.success("✅ Ulasan berhasil ditambahkan!")
            st.balloons()
    
    st.divider()
    
    # Display new reviews
    st.subheader("📋 Ulasan Baru yang Ditambahkan")
    
    total_new = sum(len(reviews) for reviews in st.session_state.new_reviews.values())
    
    if total_new == 0:
        st.info("Belum ada ulasan baru. Mulai tambahkan ulasan Anda! 👆")
    else:
        # Stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Ulasan Baru", total_new)
        with col2:
            st.metric("Positif", len(st.session_state.new_reviews['Positif']))
        with col3:
            st.metric("Netral", len(st.session_state.new_reviews['Netral']))
        with col4:
            st.metric("Negatif", len(st.session_state.new_reviews['Negatif']))
        
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
                
                st.subheader(f"{color_map[sentiment]} {sentiment} ({len(reviews)})")
                
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
        st.subheader("📥 Export Data")
        
        all_new_reviews = []
        for sentiment, reviews in st.session_state.new_reviews.items():
            for review in reviews:
                all_new_reviews.append({
                    'Sentimen': sentiment,
                    'Rating': review['stars'],
                    'Tanggal': review['date'],
                    'Ulasan': review['text']
                })
        
        if all_new_reviews:
            df_export = pd.DataFrame(all_new_reviews)
            csv = df_export.to_csv(index=False, encoding='utf-8-sig')
            
            st.download_button(
                label="📥 Download CSV",
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
st.markdown("""
<div style='text-align: center; color: #64748b; font-size: 12px;'>
    <p>D'Las Lembah Asri Sentiment Analysis Dashboard</p>
    <p>Data Source: Google Maps Reviews | Period: 2016-2024</p>
</div>
""", unsafe_allow_html=True)
